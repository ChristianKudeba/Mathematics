/* proof_viz.c — Lean Proof Visualizer (multi-document)
 *
 * Build (MSVC Developer Prompt):
 *   cl /O2 /W3 /D_CRT_SECURE_NO_WARNINGS main.c
 *     /link /SUBSYSTEM:WINDOWS user32.lib gdi32.lib comdlg32.lib msimg32.lib /OUT:proof_viz.exe
 *
 * Build (MinGW):
 *   gcc -O2 -mwindows -o proof_viz.exe main.c -lcomdlg32 -lgdi32 -luser32 -lmsimg32 -lm
 *
 * PDF support requires pdfium.dll next to proof_viz.exe.
 *
 * Controls:
 *   O        — open a .lean file
 *   P        — open a PDF
 *   T / G    — text / graph view  (lean file active)
 *   PgUp/Dn  — previous / next PDF page
 *   drag     — pan
 *   scroll   — zoom
 *   Esc      — quit
 */

#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <windowsx.h>
#include <commdlg.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>

/* ================================================================
   Constants
   ================================================================ */

#define MAX_NODES   512
#define MAX_EDGES  2048
#define NAME_LEN    128

#define NODE_W    150
#define NODE_H     40
#define LAYER_H   110
#define SLOT_W    170

#define SIDEBAR_W   230
#define BTN_H        32
#define BTN_W       190
#define BTN_X        18
#define INFO_LEN   1024

#define MAX_LEAN      8
#define MAX_PDF       8
#define FILE_ITEM_H  28    /* height of a main file row in sidebar  */
#define FILE_SUB_H   26    /* height of a PDF subrow under a lean   */
#define FILE_LIST_Y 142    /* y where the file list begins          */

/* Overlay button geometry */
#define OVL_BTN_W   120    /* PDF overlay: Prev / Next / Convert    */
#define OVL_BTN_H    34
#define OVL_BTN_GAP  12
#define OVL_TGL_W    80    /* Lean overlay: Graph / Text toggle     */
#define OVL_TGL_H    28

#define TEXT_TOP_OFFSET      50   /* gap above text-edit so lean overlay buttons stay visible */
#define SIDEBAR_COLLAPSED_W  24   /* sidebar width when collapsed */

#define CV_LINE_H   18    /* pixels per line in code view */
#define CV_LINENO_W 52    /* width of line-number gutter  */

#define NODE_PANEL_W  380  /* width of the node source panel */
#define NP_HEADER_H    40  /* height of node panel header bar */
#define NP_DIV_H       24  /* divider bar between Lean and LaTeX sections */
#define IDT_CONV_POLL 2001 /* WM_TIMER id for polling conversion process */

/* Dynamic sidebar width */
#define SW() (g_sidebar_collapsed ? SIDEBAR_COLLAPSED_W : SIDEBAR_W)

#define IDC_OPEN_LEAN     1001
#define IDC_VIEW_GRAPH    1002
#define IDC_VIEW_TEXT     1003
#define IDC_OPEN_PDF      1004
#define IDC_TEXT_VIEW     1005

/* ================================================================
   Node kinds
   ================================================================ */

typedef enum {
    NK_AXIOM = 0, NK_IMPORT, NK_DEF, NK_THEOREM, NK_LEMMA, NK_COUNT
} NodeKind;

static const COLORREF KIND_COL[NK_COUNT] = {
    RGB(180, 55, 55),
    RGB( 55,100,180),
    RGB( 55,150, 75),
    RGB( 90, 75,195),
    RGB( 55,165,165),
};
#define SORRY_COL RGB(210,140,40)

/* ================================================================
   Data model
   ================================================================ */

typedef struct {
    char     name[NAME_LEN];
    NodeKind kind;
    int      has_sorry;
    int      layer, slot, wx, wy;
    int      line_start;  /* 1-based source line; 0 = unknown (synthetic node) */
} Node;

typedef struct { int u, v; } Edge;

typedef enum { VIEW_GRAPH = 0, VIEW_TEXT, VIEW_PDF } ViewMode;

typedef struct {
    char     path[MAX_PATH];
    char     basename[64];
    Node     nd[MAX_NODES];
    int      nnd;
    Edge     ed[MAX_EDGES];
    int      ned;
    char    *text;
    float    zoom;
    int      pan_x, pan_y;
    ViewMode view_mode;
    char     status[INFO_LEN];
} LeanDoc;

typedef struct {
    char     path[MAX_PATH];
    char     basename[64];
    void    *doc;           /* FPDF_DOCUMENT (opaque)  */
    int      page_count, page_index;
    double   zoom;
    unsigned char *pixels;
    int      pw, ph, stride;
    int      pan_x, pan_y;
    BOOL     dragging;
    int      drag_x, drag_y;
    int      lean_idx;      /* -1 = not associated with any lean */
    char     status[INFO_LEN];
} PdfDoc;

static LeanDoc g_lean[MAX_LEAN];
static int     g_nlean = 0;
static PdfDoc  g_pdf[MAX_PDF];
static int     g_npdf  = 0;

typedef enum { SEL_NONE, SEL_LEAN, SEL_PDF } SelKind;
static SelKind g_sel_kind = SEL_NONE;
static int     g_sel_idx  = -1;

/* Graph-view drag */
static BOOL g_graph_dragging = FALSE;
static int  g_graph_drag_x, g_graph_drag_y;

/* ================================================================
   Sidebar drag-and-drop (PDF → Lean association)
   ================================================================ */

static int  g_drag_pdf_idx    = -1;  /* which standalone PDF is being dragged */
static int  g_drag_start_y    =  0;
static int  g_drag_cur_y      =  0;
static int  g_drag_cur_x      =  0;
static BOOL g_drag_active     = FALSE;
static int  g_drag_hover_lean = -1;  /* lean row under cursor during drag     */

/* ================================================================
   Overlay button rects (set in WM_PAINT, read in WM_LBUTTONDOWN)
   ================================================================ */

static RECT g_ovl_prev    = {0};  /* PDF: prev page     */
static RECT g_ovl_next    = {0};  /* PDF: next page     */
static RECT g_ovl_convert = {0};  /* PDF: convert paper */
static RECT g_ovl_graph   = {0};  /* Lean: graph view   */
static RECT g_ovl_text    = {0};  /* Lean: text view    */

static BOOL g_hover_prev    = FALSE;
static BOOL g_hover_next    = FALSE;
static BOOL g_hover_convert = FALSE;
static BOOL g_hover_graph   = FALSE;
static BOOL g_hover_text    = FALSE;

/* Sidebar collapse state */
static BOOL g_sidebar_collapsed  = FALSE;
static RECT g_sidebar_toggle_btn = {0};

/* Node source panel */
static HWND     g_np_hwnd        = NULL;
static WCHAR  **g_np_lines       = NULL;
static int      g_np_nlines      = 0;
static int      g_np_scroll      = 0;
static int      g_sel_node       = -1;
static char     g_np_name[NAME_LEN] = {0};
static NodeKind g_np_kind        = NK_DEF;
static RECT     g_np_close_rect  = {0};

/* LaTeX section of node panel */
static WCHAR  **g_np_tex_lines   = NULL;
static int      g_np_tex_nlines  = 0;
static int      g_np_tex_scroll  = 0;
static int      g_np_tex_state   = 0;  /* 0=idle 1=pending 2=done 3=error */
static HANDLE   g_np_conv_proc   = INVALID_HANDLE_VALUE;
static char     g_np_tex_path[MAX_PATH]  = {0};
static char     g_np_lean_path[MAX_PATH] = {0};
static char     g_np_pdf_path[MAX_PATH]  = {0};

/* Rendered bitmap for LaTeX section (pdflatex + PDFium) */
static unsigned char *g_np_tex_pixels  = NULL;
static int      g_np_tex_pw     = 0;
static int      g_np_tex_ph     = 0;
static int      g_np_tex_stride = 0;
static int      g_np_tex_pan_y  = 0;

/* Node panel resize */
static int  g_np_panel_w        = NODE_PANEL_W;
static BOOL g_np_resizing       = FALSE;
static int  g_np_resize_start_x = 0;
static int  g_np_resize_start_w = 0;
static int  g_np_char_w         = 9;  /* updated at first paint */

/* ================================================================
   PDFium dynamic loader
   ================================================================ */

typedef void*         FPDF_DOCUMENT;
typedef void*         FPDF_PAGE;
typedef void*         FPDF_BITMAP;
typedef const char*   FPDF_STRING;
typedef unsigned long FPDF_DWORD;
#ifndef FPDF_ANNOT
#define FPDF_ANNOT 0x01
#endif

typedef void          (WINAPI *PFN_FPDF_InitLibrary)(void);
typedef void          (WINAPI *PFN_FPDF_DestroyLibrary)(void);
typedef FPDF_DOCUMENT (WINAPI *PFN_FPDF_LoadDocument)(FPDF_STRING, FPDF_STRING);
typedef void          (WINAPI *PFN_FPDF_CloseDocument)(FPDF_DOCUMENT);
typedef int           (WINAPI *PFN_FPDF_GetPageCount)(FPDF_DOCUMENT);
typedef FPDF_PAGE     (WINAPI *PFN_FPDF_LoadPage)(FPDF_DOCUMENT, int);
typedef void          (WINAPI *PFN_FPDF_ClosePage)(FPDF_PAGE);
typedef double        (WINAPI *PFN_FPDF_GetPageWidth)(FPDF_PAGE);
typedef double        (WINAPI *PFN_FPDF_GetPageHeight)(FPDF_PAGE);
typedef FPDF_BITMAP   (WINAPI *PFN_FPDFBitmap_Create)(int, int, int);
typedef void          (WINAPI *PFN_FPDFBitmap_Destroy)(FPDF_BITMAP);
typedef void*         (WINAPI *PFN_FPDFBitmap_GetBuffer)(FPDF_BITMAP);
typedef int           (WINAPI *PFN_FPDFBitmap_GetStride)(FPDF_BITMAP);
typedef void          (WINAPI *PFN_FPDFBitmap_FillRect)(FPDF_BITMAP, int, int, int, int, FPDF_DWORD);
typedef void          (WINAPI *PFN_FPDF_RenderPageBitmap)(FPDF_BITMAP, FPDF_PAGE, int, int, int, int, int, int);
typedef unsigned long (WINAPI *PFN_FPDF_GetLastError)(void);

typedef struct {
    HMODULE dll; int initialized;
    PFN_FPDF_InitLibrary      InitLibrary;
    PFN_FPDF_DestroyLibrary   DestroyLibrary;
    PFN_FPDF_LoadDocument     LoadDocument;
    PFN_FPDF_CloseDocument    CloseDocument;
    PFN_FPDF_GetPageCount     GetPageCount;
    PFN_FPDF_LoadPage         LoadPage;
    PFN_FPDF_ClosePage        ClosePage;
    PFN_FPDF_GetPageWidth     GetPageWidth;
    PFN_FPDF_GetPageHeight    GetPageHeight;
    PFN_FPDFBitmap_Create     Bitmap_Create;
    PFN_FPDFBitmap_Destroy    Bitmap_Destroy;
    PFN_FPDFBitmap_GetBuffer  Bitmap_GetBuffer;
    PFN_FPDFBitmap_GetStride  Bitmap_GetStride;
    PFN_FPDFBitmap_FillRect   Bitmap_FillRect;
    PFN_FPDF_RenderPageBitmap RenderPageBitmap;
    PFN_FPDF_GetLastError     GetLastError;
} PdfiumApi;

static PdfiumApi g_pdfium = {0};

static FARPROC pdfium_proc(const char *name)
{
    return g_pdfium.dll ? GetProcAddress(g_pdfium.dll, name) : NULL;
}

static int pdfium_load(HWND hwnd)
{
    if (g_pdfium.initialized) return 1;
    g_pdfium.dll = LoadLibraryA("pdfium.dll");
    if (!g_pdfium.dll) g_pdfium.dll = LoadLibraryA("fpdf.dll");
    if (!g_pdfium.dll) {
        if (hwnd)
            MessageBoxA(hwnd,
                "Could not load PDFium.\n\n"
                "Download a Windows PDFium build and copy pdfium.dll next to proof_viz.exe.",
                "PDFium not found", MB_ICONERROR);
        return 0;
    }
    g_pdfium.InitLibrary      = (PFN_FPDF_InitLibrary)     pdfium_proc("FPDF_InitLibrary");
    g_pdfium.DestroyLibrary   = (PFN_FPDF_DestroyLibrary)  pdfium_proc("FPDF_DestroyLibrary");
    g_pdfium.LoadDocument     = (PFN_FPDF_LoadDocument)     pdfium_proc("FPDF_LoadDocument");
    g_pdfium.CloseDocument    = (PFN_FPDF_CloseDocument)    pdfium_proc("FPDF_CloseDocument");
    g_pdfium.GetPageCount     = (PFN_FPDF_GetPageCount)     pdfium_proc("FPDF_GetPageCount");
    g_pdfium.LoadPage         = (PFN_FPDF_LoadPage)         pdfium_proc("FPDF_LoadPage");
    g_pdfium.ClosePage        = (PFN_FPDF_ClosePage)        pdfium_proc("FPDF_ClosePage");
    g_pdfium.GetPageWidth     = (PFN_FPDF_GetPageWidth)     pdfium_proc("FPDF_GetPageWidth");
    g_pdfium.GetPageHeight    = (PFN_FPDF_GetPageHeight)    pdfium_proc("FPDF_GetPageHeight");
    g_pdfium.Bitmap_Create    = (PFN_FPDFBitmap_Create)     pdfium_proc("FPDFBitmap_Create");
    g_pdfium.Bitmap_Destroy   = (PFN_FPDFBitmap_Destroy)    pdfium_proc("FPDFBitmap_Destroy");
    g_pdfium.Bitmap_GetBuffer = (PFN_FPDFBitmap_GetBuffer)  pdfium_proc("FPDFBitmap_GetBuffer");
    g_pdfium.Bitmap_GetStride = (PFN_FPDFBitmap_GetStride)  pdfium_proc("FPDFBitmap_GetStride");
    g_pdfium.Bitmap_FillRect  = (PFN_FPDFBitmap_FillRect)   pdfium_proc("FPDFBitmap_FillRect");
    g_pdfium.RenderPageBitmap = (PFN_FPDF_RenderPageBitmap) pdfium_proc("FPDF_RenderPageBitmap");
    g_pdfium.GetLastError     = (PFN_FPDF_GetLastError)     pdfium_proc("FPDF_GetLastError");
    if (!g_pdfium.InitLibrary || !g_pdfium.LoadDocument || !g_pdfium.CloseDocument ||
        !g_pdfium.GetPageCount || !g_pdfium.LoadPage || !g_pdfium.ClosePage ||
        !g_pdfium.GetPageWidth || !g_pdfium.GetPageHeight || !g_pdfium.Bitmap_Create ||
        !g_pdfium.Bitmap_Destroy || !g_pdfium.Bitmap_GetBuffer ||
        !g_pdfium.Bitmap_GetStride || !g_pdfium.Bitmap_FillRect || !g_pdfium.RenderPageBitmap) {
        if (hwnd) MessageBoxA(hwnd, "Your pdfium.dll is missing a required function.", "PDFium error", MB_ICONERROR);
        FreeLibrary(g_pdfium.dll);
        memset(&g_pdfium, 0, sizeof(g_pdfium));
        return 0;
    }
    g_pdfium.InitLibrary();
    g_pdfium.initialized = 1;
    return 1;
}

/* ================================================================
   PDF helpers
   ================================================================ */

static void pdf_clear_pixels(PdfDoc *pdf)
{
    free(pdf->pixels); pdf->pixels = NULL;
    pdf->pw = pdf->ph = pdf->stride = 0;
}

static void pdf_close(PdfDoc *pdf)
{
    pdf_clear_pixels(pdf);
    if (pdf->doc && g_pdfium.CloseDocument)
        g_pdfium.CloseDocument((FPDF_DOCUMENT)pdf->doc);
    pdf->doc = NULL;
    pdf->page_count = pdf->page_index = 0;
}

static int pdf_render_page(HWND hwnd, PdfDoc *pdf)
{
    pdf_clear_pixels(pdf);
    if (!pdf->doc) return 0;
    FPDF_PAGE page = g_pdfium.LoadPage((FPDF_DOCUMENT)pdf->doc, pdf->page_index);
    if (!page) { MessageBoxA(hwnd,"Could not load page.","PDFium error",MB_ICONERROR); return 0; }
    int w = (int)(g_pdfium.GetPageWidth(page)  * pdf->zoom + 0.5); if (w < 1) w = 1;
    int h = (int)(g_pdfium.GetPageHeight(page) * pdf->zoom + 0.5); if (h < 1) h = 1;
    FPDF_BITMAP bm = g_pdfium.Bitmap_Create(w, h, 0);
    if (!bm) { g_pdfium.ClosePage(page); MessageBoxA(hwnd,"Bitmap create failed.","PDFium error",MB_ICONERROR); return 0; }
    g_pdfium.Bitmap_FillRect(bm, 0, 0, w, h, 0xFFFFFFFF);
    g_pdfium.RenderPageBitmap(bm, page, 0, 0, w, h, 0, FPDF_ANNOT);
    int ss = g_pdfium.Bitmap_GetStride(bm);
    void *src = g_pdfium.Bitmap_GetBuffer(bm);
    if (!src || ss <= 0) {
        g_pdfium.Bitmap_Destroy(bm); g_pdfium.ClosePage(page);
        MessageBoxA(hwnd,"Invalid bitmap buffer.","PDFium error",MB_ICONERROR); return 0;
    }
    int tight = w * 4;
    pdf->pixels = (unsigned char *)malloc((size_t)tight * h);
    if (!pdf->pixels) {
        g_pdfium.Bitmap_Destroy(bm); g_pdfium.ClosePage(page);
        MessageBoxA(hwnd,"Out of memory.","PDF error",MB_ICONERROR); return 0;
    }
    for (int row = 0; row < h; row++)
        memcpy(pdf->pixels + (size_t)row*tight, (unsigned char*)src + (size_t)row*ss, (size_t)tight);
    pdf->pw = w; pdf->ph = h; pdf->stride = tight;
    g_pdfium.Bitmap_Destroy(bm); g_pdfium.ClosePage(page);
    return 1;
}

static void pdf_draw_page(HDC dc, RECT vr, PdfDoc *pdf)
{
    if (!pdf->pixels || pdf->pw <= 0) {
        SetTextColor(dc,RGB(170,170,190)); SetBkMode(dc,TRANSPARENT);
        DrawTextA(dc,"Open a PDF from the sidebar.",-1,&vr,DT_CENTER|DT_VCENTER|DT_SINGLELINE);
        return;
    }
    int vw = vr.right - vr.left;
    int x = vr.left + (vw - pdf->pw)/2 + pdf->pan_x;
    int y = vr.top  + pdf->pan_y;
    RECT shadow = {x+5,y+5,x+pdf->pw+5,y+pdf->ph+5};
    HBRUSH sh = CreateSolidBrush(RGB(8,8,12)); FillRect(dc,&shadow,sh); DeleteObject(sh);
    BITMAPINFO bi; ZeroMemory(&bi,sizeof(bi));
    bi.bmiHeader.biSize=sizeof(BITMAPINFOHEADER); bi.bmiHeader.biWidth=pdf->pw;
    bi.bmiHeader.biHeight=-pdf->ph; bi.bmiHeader.biPlanes=1;
    bi.bmiHeader.biBitCount=32; bi.bmiHeader.biCompression=BI_RGB;
    StretchDIBits(dc,x,y,pdf->pw,pdf->ph,0,0,pdf->pw,pdf->ph,
                  pdf->pixels,&bi,DIB_RGB_COLORS,SRCCOPY);
}

static void pdf_change_page(HWND hwnd, PdfDoc *pdf, int delta)
{
    if (!pdf->doc) return;
    int next = pdf->page_index + delta;
    if (next < 0) next = 0;
    if (next >= pdf->page_count) next = pdf->page_count - 1;
    if (next == pdf->page_index) return;
    pdf->page_index = next;
    pdf_render_page(hwnd, pdf);
    snprintf(pdf->status,INFO_LEN,"PDF: %s\r\nPage %d of %d",
             pdf->basename, pdf->page_index+1, pdf->page_count);
    InvalidateRect(hwnd,NULL,TRUE);
}

/* ================================================================
   Graph helpers
   ================================================================ */

static int node_find(LeanDoc *doc, const char *s)
{
    for (int i = 0; i < doc->nnd; i++)
        if (strcmp(doc->nd[i].name, s) == 0) return i;
    return -1;
}

static int node_add(LeanDoc *doc, const char *s, NodeKind k)
{
    int i = node_find(doc, s);
    if (i >= 0) { if ((int)k < (int)doc->nd[i].kind) doc->nd[i].kind = k; return i; }
    if (doc->nnd >= MAX_NODES) return -1;
    i = doc->nnd++;
    strncpy(doc->nd[i].name, s, NAME_LEN-1);
    doc->nd[i].kind = k; doc->nd[i].has_sorry = 0; doc->nd[i].layer = -1;
    doc->nd[i].slot = 0; doc->nd[i].wx = 0; doc->nd[i].wy = 0;
    return i;
}

static void edge_add(LeanDoc *doc, int u, int v)
{
    if (u<0||v<0||u==v) return;
    for (int i = 0; i < doc->ned; i++) if (doc->ed[i].u==u && doc->ed[i].v==v) return;
    if (doc->ned >= MAX_EDGES) return;
    doc->ed[doc->ned].u = u; doc->ed[doc->ned].v = v; doc->ned++;
}

/* ================================================================
   Parser
   ================================================================ */

#define N_CORE_AXIOMS 4
static const char *CORE_AXIOMS[N_CORE_AXIOMS] = {
    "propext","Classical.choice","Quot.sound","funext"
};

static void rtrim(char *s) {
    int n=(int)strlen(s)-1;
    while(n>=0&&(s[n]=='\r'||s[n]=='\n'||s[n]==' '||s[n]=='\t'))s[n--]='\0';
}
static void ltrim(char *s) {
    int i=0; while(s[i]==' '||s[i]=='\t')i++;
    if(i) memmove(s,s+i,strlen(s+i)+1);
}
static const char *lex_ident(const char *src, char *dst, int dsz) {
    while(*src==' '||*src=='\t')src++;
    int i=0;
    while(*src&&*src!=' '&&*src!='\t'&&*src!='('&&*src!=')'&&
          *src!=':'&&*src!='['&&*src!='{'&&*src!=','&&i<dsz-1)
        dst[i++]=*src++;
    dst[i]='\0'; return src;
}
static int is_id_char(char c) {
    return (c>='a'&&c<='z')||(c>='A'&&c<='Z')||(c>='0'&&c<='9')||c=='_'||c=='.';
}
static int word_in(const char *hay, const char *needle) {
    int nlen=(int)strlen(needle); if(!nlen) return 0;
    const char *p=hay;
    while((p=strstr(p,needle))!=NULL){
        char before=(p>hay)?p[-1]:'\0', after=p[nlen];
        if(!is_id_char(before)&&!is_id_char(after)) return 1;
        p+=nlen;
    }
    return 0;
}
static const char *skip_modifiers(const char *p) {
    again:
    while(*p==' '||*p=='\t')p++;
    if(*p=='@'){const char *cl=strchr(p,']');if(cl){p=cl+1;goto again;}}
    static const char *mods[]={"noncomputable ","private ","protected ",
                                "partial ","unsafe ","scoped ","irreducible "};
    for(int m=0;m<7;m++){size_t ml=strlen(mods[m]);if(strncmp(p,mods[m],ml)==0){p+=ml;goto again;}}
    return p;
}
static int decl_keyword(const char *p, NodeKind *kind) {
    struct{const char *kw;NodeKind k;}kws[]={
        {"theorem ",NK_THEOREM},{"lemma ",NK_LEMMA},{"def ",NK_DEF},
        {"abbrev ",NK_DEF},{"axiom ",NK_AXIOM},{"opaque ",NK_DEF}};
    for(int i=0;i<6;i++){size_t l=strlen(kws[i].kw);if(strncmp(p,kws[i].kw,l)==0){*kind=kws[i].k;return(int)l;}}
    return 0;
}

static void parse_file(LeanDoc *doc, const char *path)
{
    doc->nnd=0; doc->ned=0;
    for(int i=0;i<N_CORE_AXIOMS;i++) node_add(doc,CORE_AXIOMS[i],NK_AXIOM);
    FILE *f=fopen(path,"r"); if(!f) return;
    char line[4096];
    int in_block=0, line_num=0;
    while(fgets(line,sizeof(line),f)){
        line_num++;
        rtrim(line); ltrim(line);
        if(in_block){if(strstr(line,"-/"))in_block=0;continue;}
        if(line[0]=='/'&&line[1]=='-'){if(!strstr(line,"-/"))in_block=1;continue;}
        if(line[0]=='-'&&line[1]=='-')continue;
        if(line[0]=='/'&&line[1]=='*')continue;
        if(strncmp(line,"import ",7)==0){
            char nm[NAME_LEN];lex_ident(line+7,nm,NAME_LEN);
            if(nm[0]){node_add(doc,nm,NK_IMPORT);int idx=node_find(doc,nm);if(idx>=0)doc->nd[idx].line_start=line_num;}
            continue;
        }
        const char *p=skip_modifiers(line);NodeKind k;int kl=decl_keyword(p,&k);
        if(!kl)continue;
        char nm[NAME_LEN];lex_ident(p+kl,nm,NAME_LEN);
        if(nm[0]){node_add(doc,nm,k);int idx=node_find(doc,nm);if(idx>=0)doc->nd[idx].line_start=line_num;}
    }
    rewind(f);int cur=-1;in_block=0;
    while(fgets(line,sizeof(line),f)){
        rtrim(line);ltrim(line);
        if(in_block){if(strstr(line,"-/"))in_block=0;continue;}
        if(line[0]=='/'&&line[1]=='-'){if(!strstr(line,"-/"))in_block=1;continue;}
        if(line[0]=='-'&&line[1]=='-')continue;
        const char *p=skip_modifiers(line);NodeKind k;int kl=0;
        if(strncmp(line,"import ",7)==0){char nm[NAME_LEN];lex_ident(line+7,nm,NAME_LEN);cur=node_find(doc,nm);kl=1;}
        else{kl=decl_keyword(p,&k);if(kl){char nm[NAME_LEN];lex_ident(p+kl,nm,NAME_LEN);cur=node_find(doc,nm);}}
        if(cur<0)continue;
        if(strstr(line,"sorry"))doc->nd[cur].has_sorry=1;
        for(int i=0;i<doc->nnd;i++){if(i==cur)continue;if(word_in(line,doc->nd[i].name))edge_add(doc,cur,i);}
    }
    fclose(f);
    for(int i=0;i<doc->nnd;i++)
        if(doc->nd[i].kind==NK_IMPORT)
            for(int j=0;j<N_CORE_AXIOMS;j++) edge_add(doc,i,node_find(doc,CORE_AXIOMS[j]));
}

/* ================================================================
   Layout
   ================================================================ */

static void layout(LeanDoc *doc)
{
    int layer_sz[MAX_NODES]; memset(layer_sz,0,sizeof(layer_sz));
    for(int i=0;i<doc->nnd;i++) doc->nd[i].layer=-1;
    for(int i=0;i<doc->nnd;i++) if(doc->nd[i].kind==NK_AXIOM) doc->nd[i].layer=0;
    int changed=1;
    while(changed){
        changed=0;
        for(int e=0;e<doc->ned;e++){
            int u=doc->ed[e].u,v=doc->ed[e].v;
            if(doc->nd[v].layer<0)continue;
            int want=doc->nd[v].layer+1;
            if(doc->nd[u].layer<want){doc->nd[u].layer=want;changed=1;}
        }
    }
    for(int i=0;i<doc->nnd;i++) if(doc->nd[i].layer<0) doc->nd[i].layer=1;
    int max_layer=0;
    for(int i=0;i<doc->nnd;i++) if(doc->nd[i].layer>max_layer) max_layer=doc->nd[i].layer;
    for(int i=0;i<doc->nnd;i++) doc->nd[i].slot=layer_sz[doc->nd[i].layer]++;
    int max_in_layer=0;
    for(int i=0;i<=max_layer;i++) if(layer_sz[i]>max_in_layer) max_in_layer=layer_sz[i];
    for(int i=0;i<doc->nnd;i++){
        int lsz=layer_sz[doc->nd[i].layer];
        int offset=(max_in_layer*SLOT_W-lsz*SLOT_W)/2;
        doc->nd[i].wx=offset+doc->nd[i].slot*SLOT_W;
        doc->nd[i].wy=(max_layer-doc->nd[i].layer)*LAYER_H;
    }
}

/* ================================================================
   Renderer
   ================================================================ */

static void w2s(LeanDoc *doc, int wx, int wy, int *sx, int *sy)
{
    *sx=SW()+(int)(wx*doc->zoom)+doc->pan_x;
    *sy=(int)(wy*doc->zoom)+doc->pan_y;
}

static char *extract_node_source(LeanDoc *doc, int node_idx)
{
    if(!doc->text||node_idx<0||node_idx>=doc->nnd) return NULL;
    int target=doc->nd[node_idx].line_start;
    if(target<=0) return NULL;
    const char *p=doc->text;
    for(int l=1;l<target&&*p;p++) if(*p=='\n') l++;
    const char *src_start=p;
    const char *src_end=p;
    const char *q=p;
    int first=1;
    while(*q){
        const char *ls=q;
        while(*q&&*q!='\n') q++;
        if(*q=='\n') q++;
        if(!first&&*ls!=' '&&*ls!='\t'&&*ls!='\0'&&*ls!='\n'){
            char tmp[512];int ll=(int)(q-ls);if(ll>511)ll=511;
            memcpy(tmp,ls,ll);tmp[ll]='\0';
            char *nl2=strchr(tmp,'\n');if(nl2)*nl2='\0';
            char *cr2=strchr(tmp,'\r');if(cr2)*cr2='\0';
            const char *sp=skip_modifiers(tmp);
            NodeKind kk;
            if(decl_keyword(sp,&kk)){src_end=ls;break;}
            if(strncmp(tmp,"namespace ",10)==0||strncmp(tmp,"section ",8)==0||
               strncmp(tmp,"end ",4)==0||strcmp(tmp,"end")==0){src_end=ls;break;}
        }
        src_end=q;
        first=0;
    }
    int len=(int)(src_end-src_start);
    while(len>0&&(src_start[len-1]=='\n'||src_start[len-1]=='\r'||
                  src_start[len-1]==' '||src_start[len-1]=='\t')) len--;
    if(len<=0){
        const char fb[]="(source not available)";
        char *r2=(char*)malloc(sizeof(fb));memcpy(r2,fb,sizeof(fb));return r2;
    }
    char *r=(char*)malloc(len+1);
    memcpy(r,src_start,len);r[len]='\0';
    return r;
}

static int node_hit_test(LeanDoc *doc, int sx, int sy)
{
    for(int i=0;i<doc->nnd;i++){
        int x1,y1,x2,y2;
        w2s(doc,doc->nd[i].wx,        doc->nd[i].wy,        &x1,&y1);
        w2s(doc,doc->nd[i].wx+NODE_W, doc->nd[i].wy+NODE_H, &x2,&y2);
        if(sx>=x1&&sx<x2&&sy>=y1&&sy<y2) return i;
    }
    return -1;
}

static void draw_arrow(HDC dc,int x1,int y1,int x2,int y2,COLORREF col)
{
    HPEN pen=CreatePen(PS_SOLID,1,col),old=(HPEN)SelectObject(dc,pen);
    MoveToEx(dc,x1,y1,NULL);LineTo(dc,x2,y2);
    double dx=x2-x1,dy=y2-y1,len=sqrt(dx*dx+dy*dy);
    if(len>1.0){dx/=len;dy/=len;int al=9;
        MoveToEx(dc,x2,y2,NULL);LineTo(dc,x2-(int)(al*(dx+dy*0.5)),y2-(int)(al*(dy-dx*0.5)));
        MoveToEx(dc,x2,y2,NULL);LineTo(dc,x2-(int)(al*(dx-dy*0.5)),y2-(int)(al*(dy+dx*0.5)));}
    SelectObject(dc,old);DeleteObject(pen);
}

static void draw_node(HDC dc, LeanDoc *doc, int i)
{
    int sx,sy; w2s(doc,doc->nd[i].wx,doc->nd[i].wy,&sx,&sy);
    int w=(int)(NODE_W*doc->zoom),h=(int)(NODE_H*doc->zoom);
    COLORREF bg=doc->nd[i].has_sorry?SORRY_COL:KIND_COL[doc->nd[i].kind];
    HBRUSH br=CreateSolidBrush(bg);HPEN pn=CreatePen(PS_SOLID,1,RGB(220,220,220));
    HBRUSH obr=(HBRUSH)SelectObject(dc,br);HPEN opn=(HPEN)SelectObject(dc,pn);
    RoundRect(dc,sx,sy,sx+w,sy+h,10,10);
    SelectObject(dc,obr);SelectObject(dc,opn);DeleteObject(br);DeleteObject(pn);
    SetTextColor(dc,RGB(255,255,255));SetBkMode(dc,TRANSPARENT);
    RECT tr={sx+4,sy,sx+w-4,sy+h};
    DrawTextA(dc,doc->nd[i].name,-1,&tr,DT_CENTER|DT_VCENTER|DT_SINGLELINE|DT_END_ELLIPSIS);
}

static void draw_graph(HDC dc, LeanDoc *doc)
{
    for(int e=0;e<doc->ned;e++){
        int u=doc->ed[e].u,v=doc->ed[e].v,tx,ty,hx,hy;
        w2s(doc,doc->nd[v].wx+NODE_W/2,doc->nd[v].wy,      &tx,&ty);
        w2s(doc,doc->nd[u].wx+NODE_W/2,doc->nd[u].wy+NODE_H,&hx,&hy);
        draw_arrow(dc,tx,ty,hx,hy,RGB(120,120,140));
    }
    for(int i=0;i<doc->nnd;i++) draw_node(dc,doc,i);
    if(g_sel_node>=0&&g_sel_node<doc->nnd){
        int sx2,sy2;w2s(doc,doc->nd[g_sel_node].wx,doc->nd[g_sel_node].wy,&sx2,&sy2);
        int nw=(int)(NODE_W*doc->zoom),nh=(int)(NODE_H*doc->zoom);
        HPEN hlp=CreatePen(PS_SOLID,2,RGB(255,255,255));
        HPEN ohlp=(HPEN)SelectObject(dc,hlp);
        SelectObject(dc,GetStockObject(NULL_BRUSH));
        RoundRect(dc,sx2-2,sy2-2,sx2+nw+2,sy2+nh+2,12,12);
        SelectObject(dc,ohlp);DeleteObject(hlp);
    }
}

static void draw_legend(HDC dc, int left, int top)
{
    struct{const char *label;COLORREF col;}e[]={
        {"axiom",KIND_COL[NK_AXIOM]},{"import",KIND_COL[NK_IMPORT]},
        {"def / abbrev",KIND_COL[NK_DEF]},{"theorem",KIND_COL[NK_THEOREM]},
        {"lemma",KIND_COL[NK_LEMMA]},{"uses sorry",SORRY_COL}};
    for(int i=0;i<6;i++){
        HBRUSH b=CreateSolidBrush(e[i].col);HPEN p=CreatePen(PS_SOLID,1,RGB(200,200,200));
        SelectObject(dc,b);SelectObject(dc,p);
        RoundRect(dc,left,top+i*20,left+14,top+i*20+13,3,3);
        DeleteObject(b);DeleteObject(p);
        SetTextColor(dc,RGB(180,180,200));SetBkMode(dc,TRANSPARENT);
        TextOutA(dc,left+18,top+i*20,e[i].label,(int)strlen(e[i].label));
    }
}

/* ================================================================
   Overlay button drawing (semi-transparent, uses AlphaBlend)
   ================================================================ */

static void draw_overlay_btn(HDC dc, RECT r, const char *label, BOOL hover, BOOL active)
{
    int w = r.right-r.left, h = r.bottom-r.top;
    if (w <= 0 || h <= 0) return;

    HDC     bdc  = CreateCompatibleDC(dc);
    HBITMAP bbmp = CreateCompatibleBitmap(dc, w, h);
    HBITMAP bold = (HBITMAP)SelectObject(bdc, bbmp);

    /* fill */
    COLORREF bg = active ? RGB(75,88,138) : (hover ? RGB(52,62,100) : RGB(24,28,48));
    HBRUSH br = CreateSolidBrush(bg);
    RECT lr = {0,0,w,h};
    FillRect(bdc, &lr, br); DeleteObject(br);

    /* border */
    HPEN pn = CreatePen(PS_SOLID, 1, active ? RGB(120,140,210) : RGB(65,75,120));
    HPEN opn = (HPEN)SelectObject(bdc, pn);
    HBRUSH obr = (HBRUSH)SelectObject(bdc, GetStockObject(NULL_BRUSH));
    RoundRect(bdc, 0, 0, w, h, 6, 6);
    SelectObject(bdc, opn); DeleteObject(pn);
    SelectObject(bdc, obr);

    /* label */
    HFONT font = CreateFontA(13,0,0,0,FW_NORMAL,0,0,0,DEFAULT_CHARSET,
                             OUT_DEFAULT_PRECIS,CLIP_DEFAULT_PRECIS,
                             CLEARTYPE_QUALITY,DEFAULT_PITCH,"Segoe UI");
    HFONT ofont = (HFONT)SelectObject(bdc, font);
    SetTextColor(bdc, active ? RGB(255,255,255) : RGB(200,208,238));
    SetBkMode(bdc, TRANSPARENT);
    DrawTextA(bdc, label, -1, &lr, DT_CENTER|DT_VCENTER|DT_SINGLELINE);
    SelectObject(bdc, ofont); DeleteObject(font);

    BLENDFUNCTION bf = {AC_SRC_OVER, 0, 195, 0};
    AlphaBlend(dc, r.left, r.top, w, h, bdc, 0, 0, w, h, bf);

    SelectObject(bdc, bold); DeleteObject(bbmp); DeleteDC(bdc);
}

/* Compute and draw PDF overlay buttons; stores rects for hit-testing */
static void draw_pdf_overlays(HDC dc, RECT vr)
{
    int total_w = 3*OVL_BTN_W + 2*OVL_BTN_GAP;
    int cx = vr.left + (vr.right - vr.left)/2;
    int bx = cx - total_w/2;
    int by = vr.bottom - OVL_BTN_H - 16;

    g_ovl_prev    = (RECT){bx,                        by, bx+OVL_BTN_W,               by+OVL_BTN_H};
    g_ovl_next    = (RECT){bx+OVL_BTN_W+OVL_BTN_GAP, by, bx+2*OVL_BTN_W+OVL_BTN_GAP, by+OVL_BTN_H};
    g_ovl_convert = (RECT){bx+2*(OVL_BTN_W+OVL_BTN_GAP), by, bx+3*OVL_BTN_W+2*OVL_BTN_GAP, by+OVL_BTN_H};

    draw_overlay_btn(dc, g_ovl_prev,    "Prev Page",     g_hover_prev,    FALSE);
    draw_overlay_btn(dc, g_ovl_next,    "Next Page",     g_hover_next,    FALSE);
    draw_overlay_btn(dc, g_ovl_convert, "Convert Paper", g_hover_convert, FALSE);
}

/* Compute and draw Lean overlay buttons (Graph/Text toggle) */
static void draw_lean_overlays(HDC dc, RECT vr, ViewMode cur_mode)
{
    int rx = vr.right - 12;
    int ty = vr.top + 12;

    g_ovl_text  = (RECT){rx - OVL_TGL_W,                ty, rx,                ty+OVL_TGL_H};
    g_ovl_graph = (RECT){rx - 2*OVL_TGL_W - OVL_BTN_GAP, ty, rx-OVL_TGL_W-OVL_BTN_GAP, ty+OVL_TGL_H};

    draw_overlay_btn(dc, g_ovl_graph, "Graph", g_hover_graph, cur_mode == VIEW_GRAPH);
    draw_overlay_btn(dc, g_ovl_text,  "Text",  g_hover_text,  cur_mode == VIEW_TEXT);
}

/* ================================================================
   Sidebar: file list (lean-centric: PDFs are subrows of their lean)
   ================================================================ */

/* Shared kernel: draw when dc!=NULL, hit-test when hit_y>=0.
   Returns 1 and sets *out_kind/*out_idx on hit. */
static int sidebar_iter(HDC dc, int cr_bottom, int hit_y,
                        SelKind *out_kind, int *out_idx)
{
    HFONT small = NULL, old_font = NULL;
    if (dc) {
        small = CreateFontA(12,0,0,0,FW_NORMAL,0,0,0,DEFAULT_CHARSET,
                            OUT_DEFAULT_PRECIS,CLIP_DEFAULT_PRECIS,
                            CLEARTYPE_QUALITY,DEFAULT_PITCH,"Segoe UI");
        old_font = (HFONT)SelectObject(dc, small);
    }

    int y = FILE_LIST_Y;

    /* ---- "Open Files" section header ---- */
    if (g_nlean > 0 || g_npdf > 0) {
        if (dc) {
            SetTextColor(dc,RGB(100,105,135));SetBkMode(dc,TRANSPARENT);
            RECT hr={BTN_X,y,SIDEBAR_W-8,y+15};
            DrawTextA(dc,"Open Files",-1,&hr,DT_LEFT|DT_VCENTER|DT_SINGLELINE);
        }
        y += 17;
    }

    for (int i = 0; i < g_nlean && y < cr_bottom-110; i++) {
        /* lean row hit-test */
        if (hit_y >= y && hit_y < y+FILE_ITEM_H) {
            if (out_kind) *out_kind = SEL_LEAN;
            if (out_idx)  *out_idx  = i;
            if (dc) { SelectObject(dc,old_font); DeleteObject(small); }
            return 1;
        }

        if (dc) {
            BOOL sel = (g_sel_kind==SEL_LEAN && g_sel_idx==i);
            BOOL drop_target = (g_drag_active && g_drag_hover_lean==i);

            /* row background */
            if (sel || drop_target) {
                RECT ir={BTN_X-2,y,SIDEBAR_W-6,y+FILE_ITEM_H};
                HBRUSH hi=CreateSolidBrush(drop_target?RGB(40,80,50):RGB(55,65,95));
                FillRect(dc,&ir,hi); DeleteObject(hi);
            }
            if (drop_target) {
                /* draw a dashed drop-target border */
                HPEN dp=CreatePen(PS_DOT,1,RGB(80,200,100));
                HPEN odp=(HPEN)SelectObject(dc,dp);
                HBRUSH obr=(HBRUSH)SelectObject(dc,GetStockObject(NULL_BRUSH));
                Rectangle(dc,BTN_X-2,y,SIDEBAR_W-6,y+FILE_ITEM_H);
                SelectObject(dc,odp);DeleteObject(dp);SelectObject(dc,obr);
            }

            /* lean icon — indigo */
            HBRUSH ib=CreateSolidBrush(KIND_COL[NK_THEOREM]);
            HPEN   ip=CreatePen(PS_SOLID,0,KIND_COL[NK_THEOREM]);
            SelectObject(dc,ib);SelectObject(dc,ip);
            Rectangle(dc,BTN_X,y+9,BTN_X+10,y+19);
            DeleteObject(ib);DeleteObject(ip);
            SetTextColor(dc,sel?RGB(255,255,255):RGB(200,205,225));
            SetBkMode(dc,TRANSPARENT);
            RECT tr={BTN_X+14,y,SIDEBAR_W-22,y+FILE_ITEM_H};
            DrawTextA(dc,g_lean[i].basename,-1,&tr,DT_LEFT|DT_VCENTER|DT_SINGLELINE|DT_END_ELLIPSIS);
            /* close button */
            SetTextColor(dc,sel?RGB(200,80,80):RGB(70,72,90));
            RECT xr={SIDEBAR_W-20,y+5,SIDEBAR_W-5,y+FILE_ITEM_H-5};
            DrawTextA(dc,"x",-1,&xr,DT_CENTER|DT_VCENTER|DT_SINGLELINE);
        }
        y += FILE_ITEM_H;

        /* ---- PDF subrows under this lean ---- */
        for (int j = 0; j < g_npdf && y < cr_bottom-110; j++) {
            if (g_pdf[j].lean_idx != i) continue;

            /* PDF subrow hit-test */
            if (hit_y >= y && hit_y < y+FILE_SUB_H) {
                if (out_kind) *out_kind = SEL_PDF;
                if (out_idx)  *out_idx  = j;
                if (dc) { SelectObject(dc,old_font); DeleteObject(small); }
                return 1;
            }

            if (dc) {
                BOOL sel2 = (g_sel_kind==SEL_PDF && g_sel_idx==j);
                if (sel2) {
                    RECT ir2={BTN_X+8,y,SIDEBAR_W-6,y+FILE_SUB_H};
                    HBRUSH hi2=CreateSolidBrush(RGB(55,65,95));
                    FillRect(dc,&ir2,hi2); DeleteObject(hi2);
                }
                /* PDF icon — orange (indented) */
                HBRUSH ib2=CreateSolidBrush(RGB(200,85,45));
                HPEN   ip2=CreatePen(PS_SOLID,0,RGB(200,85,45));
                SelectObject(dc,ib2);SelectObject(dc,ip2);
                Rectangle(dc,BTN_X+10,y+7,BTN_X+19,y+FILE_SUB_H-5);
                DeleteObject(ib2);DeleteObject(ip2);
                SetTextColor(dc,sel2?RGB(255,255,255):RGB(180,185,205));
                SetBkMode(dc,TRANSPARENT);
                RECT sr={BTN_X+23,y,SIDEBAR_W-22,y+FILE_SUB_H};
                DrawTextA(dc,g_pdf[j].basename,-1,&sr,DT_LEFT|DT_VCENTER|DT_SINGLELINE|DT_END_ELLIPSIS);
                /* close button */
                SetTextColor(dc,sel2?RGB(200,80,80):RGB(70,72,90));
                RECT xr2={SIDEBAR_W-20,y+3,SIDEBAR_W-5,y+FILE_SUB_H-3};
                DrawTextA(dc,"x",-1,&xr2,DT_CENTER|DT_VCENTER|DT_SINGLELINE);
            }
            y += FILE_SUB_H;
        }
    }

    /* ---- Standalone PDFs (lean_idx == -1) ---- */
    int has_standalone = 0;
    for (int j = 0; j < g_npdf; j++) if (g_pdf[j].lean_idx < 0) { has_standalone = 1; break; }
    if (has_standalone && g_nlean > 0) y += 4;

    for (int j = 0; j < g_npdf && y < cr_bottom-110; j++) {
        if (g_pdf[j].lean_idx >= 0) continue;

        /* standalone PDF hit-test */
        if (hit_y >= y && hit_y < y+FILE_ITEM_H) {
            if (out_kind) *out_kind = SEL_PDF;
            if (out_idx)  *out_idx  = j;
            if (dc) { SelectObject(dc,old_font); DeleteObject(small); }
            return 1;
        }

        if (dc) {
            BOOL sel = (g_sel_kind==SEL_PDF && g_sel_idx==j);
            BOOL is_dragged = (g_drag_pdf_idx==j && g_drag_active);

            if (sel && !is_dragged) {
                RECT ir={BTN_X-2,y,SIDEBAR_W-6,y+FILE_ITEM_H};
                HBRUSH hi=CreateSolidBrush(RGB(55,65,95));
                FillRect(dc,&ir,hi); DeleteObject(hi);
            }

            /* pdf icon */
            BYTE alpha = is_dragged ? 100 : 255;
            COLORREF icon_col = RGB(200,85,45);
            HBRUSH ib=CreateSolidBrush(icon_col);
            HPEN   ip=CreatePen(PS_SOLID,0,icon_col);
            SelectObject(dc,ib);SelectObject(dc,ip);
            Rectangle(dc,BTN_X,y+9,BTN_X+10,y+19);
            DeleteObject(ib);DeleteObject(ip);
            (void)alpha; /* icon color dimming could use GDI+ — skip for simplicity */
            SetTextColor(dc,is_dragged?RGB(100,100,110):(sel?RGB(255,255,255):RGB(200,205,225)));
            SetBkMode(dc,TRANSPARENT);
            RECT tr={BTN_X+14,y,SIDEBAR_W-22,y+FILE_ITEM_H};
            DrawTextA(dc,g_pdf[j].basename,-1,&tr,DT_LEFT|DT_VCENTER|DT_SINGLELINE|DT_END_ELLIPSIS);
            /* close button */
            SetTextColor(dc,sel?RGB(200,80,80):RGB(70,72,90));
            RECT xr={SIDEBAR_W-20,y+5,SIDEBAR_W-5,y+FILE_ITEM_H-5};
            DrawTextA(dc,"x",-1,&xr,DT_CENTER|DT_VCENTER|DT_SINGLELINE);
        }
        y += FILE_ITEM_H;
    }

    /* ---- Drag ghost (floating label near cursor) ---- */
    if (dc && g_drag_active && g_drag_pdf_idx >= 0) {
        int gx = BTN_X + 4, gy = g_drag_cur_y - FILE_ITEM_H/2;
        if (gy < FILE_LIST_Y) gy = FILE_LIST_Y;
        RECT gr = {gx, gy, SIDEBAR_W-10, gy+FILE_ITEM_H};
        HBRUSH gb = CreateSolidBrush(RGB(45,50,80));
        FillRect(dc, &gr, gb); DeleteObject(gb);
        HPEN gp = CreatePen(PS_SOLID,1,RGB(80,90,140));
        HPEN ogp=(HPEN)SelectObject(dc,gp);
        HBRUSH obr2=(HBRUSH)SelectObject(dc,GetStockObject(NULL_BRUSH));
        Rectangle(dc,gx,gy,SIDEBAR_W-10,gy+FILE_ITEM_H);
        SelectObject(dc,ogp);DeleteObject(gp);SelectObject(dc,obr2);
        /* pdf icon */
        HBRUSH ib=CreateSolidBrush(RGB(200,85,45));
        HPEN   ip=CreatePen(PS_SOLID,0,RGB(200,85,45));
        SelectObject(dc,ib);SelectObject(dc,ip);
        Rectangle(dc,gx+2,gy+9,gx+12,gy+19);
        DeleteObject(ib);DeleteObject(ip);
        SetTextColor(dc,RGB(220,220,240));SetBkMode(dc,TRANSPARENT);
        RECT gt={gx+16,gy,SIDEBAR_W-12,gy+FILE_ITEM_H};
        DrawTextA(dc,g_pdf[g_drag_pdf_idx].basename,-1,&gt,
                  DT_LEFT|DT_VCENTER|DT_SINGLELINE|DT_END_ELLIPSIS);
    }

    if (dc) { SelectObject(dc,old_font); DeleteObject(small); }
    return 0;
}

static void draw_file_list(HDC dc, int cr_bottom)
{
    sidebar_iter(dc, cr_bottom, -1, NULL, NULL);
}

static int sidebar_hit(int mouse_y, SelKind *out_kind, int *out_idx)
{
    return sidebar_iter(NULL, 9999, mouse_y, out_kind, out_idx);
}

/* During a drag, find which lean row is under the cursor */
static int sidebar_hover_lean(int mouse_y)
{
    int y = FILE_LIST_Y;
    if (g_nlean > 0) y += 17;
    for (int i = 0; i < g_nlean; i++) {
        if (mouse_y >= y && mouse_y < y+FILE_ITEM_H) return i;
        y += FILE_ITEM_H;
        for (int j = 0; j < g_npdf; j++) {
            if (g_pdf[j].lean_idx != i) continue;
            y += FILE_SUB_H;
        }
    }
    return -1;
}

/* ================================================================
   Win32 child controls
   ================================================================ */

static HWND g_hwnd;
static HWND g_btn_open_lean;
static HWND g_btn_open_pdf;
static HFONT g_ui_font;
static HFONT g_mono_font;

/* Code view (replaces EDIT control) */
static HWND   g_cv_hwnd   = NULL;
static WCHAR **g_cv_lines = NULL;
static int     g_cv_nlines= 0;
static int     g_cv_scroll= 0;

/* ================================================================
   Utilities
   ================================================================ */

static int has_ext(const char *path, const char *ext)
{
    size_t lp=strlen(path),le=strlen(ext);
    if(lp<le)return 0;
    return lstrcmpiA(path+lp-le,ext)==0;
}

static void get_basename(const char *path, char *out, int outsz)
{
    const char *s1=strrchr(path,'\\'),*s2=strrchr(path,'/');
    const char *s=(s1>s2)?s1:s2;
    strncpy(out,s?s+1:path,outsz-1);out[outsz-1]='\0';
}

static int read_entire_file(const char *path, char **out, DWORD *out_len)
{
    HANDLE h=CreateFileA(path,GENERIC_READ,FILE_SHARE_READ,NULL,
                         OPEN_EXISTING,FILE_ATTRIBUTE_NORMAL,NULL);
    if(h==INVALID_HANDLE_VALUE)return 0;
    LARGE_INTEGER size;
    if(!GetFileSizeEx(h,&size)||size.QuadPart>50*1024*1024){CloseHandle(h);return 0;}
    DWORD len=(DWORD)size.QuadPart;
    char *buf=(char*)malloc(len+1);
    if(!buf){CloseHandle(h);return 0;}
    DWORD got=0;BOOL ok=ReadFile(h,buf,len,&got,NULL);CloseHandle(h);
    if(!ok){free(buf);return 0;}
    buf[got]='\0';*out=buf;if(out_len)*out_len=got;return 1;
}

/* ================================================================
   Document management
   ================================================================ */

static int lean_open(HWND hwnd, const char *path)
{
    for(int i=0;i<g_nlean;i++) if(lstrcmpiA(g_lean[i].path,path)==0)return i;
    if(g_nlean>=MAX_LEAN){
        MessageBoxA(hwnd,"Maximum lean files already open.","Limit",MB_ICONWARNING);
        return -1;
    }
    int idx=g_nlean++;
    LeanDoc *doc=&g_lean[idx];
    memset(doc,0,sizeof(*doc));
    strncpy(doc->path,path,MAX_PATH-1);
    get_basename(path,doc->basename,sizeof(doc->basename));
    doc->zoom=1.0f;doc->pan_x=60;doc->pan_y=40;
    doc->view_mode=VIEW_GRAPH;
    parse_file(doc,path);
    layout(doc);
    char *text=NULL;DWORD len=0;
    if(read_entire_file(path,&text,&len))doc->text=text;
    snprintf(doc->status,INFO_LEN,"Lean: %s\r\n\r\nNodes: %d\r\nEdges: %d",
             doc->basename,doc->nnd,doc->ned);
    return idx;
}

static int pdf_open_doc(HWND hwnd, const char *path)
{
    for(int i=0;i<g_npdf;i++) if(lstrcmpiA(g_pdf[i].path,path)==0)return i;
    if(!pdfium_load(hwnd))return -1;
    if(g_npdf>=MAX_PDF){
        MessageBoxA(hwnd,"Maximum PDFs already open.","Limit",MB_ICONWARNING);
        return -1;
    }
    int idx=g_npdf++;
    PdfDoc *pdf=&g_pdf[idx];
    memset(pdf,0,sizeof(*pdf));
    pdf->lean_idx=-1;pdf->zoom=1.25;pdf->pan_y=20;
    strncpy(pdf->path,path,MAX_PATH-1);
    get_basename(path,pdf->basename,sizeof(pdf->basename));
    pdf->doc=g_pdfium.LoadDocument(path,NULL);
    if(!pdf->doc){
        unsigned long err=g_pdfium.GetLastError?g_pdfium.GetLastError():0;
        char msg[256];snprintf(msg,sizeof(msg),"PDFium error: %lu",err);
        MessageBoxA(hwnd,msg,"PDFium error",MB_ICONERROR);
        g_npdf--;return -1;
    }
    pdf->page_count=g_pdfium.GetPageCount((FPDF_DOCUMENT)pdf->doc);
    pdf_render_page(hwnd,pdf);
    snprintf(pdf->status,INFO_LEN,"PDF: %s\r\nPage 1 of %d",
             pdf->basename,pdf->page_count);
    return idx;
}

/* ================================================================
   Code view — UTF-8 aware line-numbered text display
   ================================================================ */

static void code_view_free(void)
{
    if(!g_cv_lines) return;
    for(int i=0;i<g_cv_nlines;i++) free(g_cv_lines[i]);
    free(g_cv_lines);
    g_cv_lines=NULL; g_cv_nlines=0;
}

static void code_view_load(const char *utf8)
{
    code_view_free();
    if(!utf8||!*utf8) return;
    int wlen=MultiByteToWideChar(CP_UTF8,0,utf8,-1,NULL,0);
    WCHAR *wide=(WCHAR*)malloc(wlen*sizeof(WCHAR));
    MultiByteToWideChar(CP_UTF8,0,utf8,-1,wide,wlen);
    int n=1;
    for(WCHAR *p=wide;*p;p++) if(*p==L'\n') n++;
    g_cv_lines=(WCHAR**)malloc(n*sizeof(WCHAR*));
    g_cv_nlines=0;
    WCHAR *start=wide;
    for(WCHAR *p=wide;;p++){
        if(*p==L'\n'||*p==L'\0'){
            int len=(int)(p-start);
            if(len>0&&start[len-1]==L'\r') len--;
            WCHAR *line=(WCHAR*)malloc((len+1)*sizeof(WCHAR));
            if(len) wcsncpy(line,start,len);
            line[len]=L'\0';
            g_cv_lines[g_cv_nlines++]=line;
            if(*p==L'\0') break;
            start=p+1;
        }
    }
    free(wide);
    g_cv_scroll=0;
    if(g_cv_hwnd){
        RECT cr;GetClientRect(g_cv_hwnd,&cr);
        int vis=cr.bottom/CV_LINE_H;
        SCROLLINFO si={sizeof(si),SIF_RANGE|SIF_PAGE|SIF_POS,0,
                       g_cv_nlines>0?g_cv_nlines-1:0,(UINT)vis,0,0};
        SetScrollInfo(g_cv_hwnd,SB_VERT,&si,TRUE);
        InvalidateRect(g_cv_hwnd,NULL,TRUE);
    }
}

static LRESULT CALLBACK CodeViewWndProc(HWND hwnd,UINT msg,WPARAM wp,LPARAM lp)
{
    switch(msg){
    case WM_PAINT:{
        PAINTSTRUCT ps;HDC hdc=BeginPaint(hwnd,&ps);
        RECT cr;GetClientRect(hwnd,&cr);
        HDC mdc=CreateCompatibleDC(hdc);
        HBITMAP bmp=CreateCompatibleBitmap(hdc,cr.right,cr.bottom);
        SelectObject(mdc,bmp);
        HBRUSH bg=CreateSolidBrush(RGB(30,30,30));FillRect(mdc,&cr,bg);DeleteObject(bg);
        RECT gutter={0,0,CV_LINENO_W,cr.bottom};
        HBRUSH gb=CreateSolidBrush(RGB(24,24,24));FillRect(mdc,&gutter,gb);DeleteObject(gb);
        HPEN sep=CreatePen(PS_SOLID,1,RGB(50,50,50));
        HPEN osep=(HPEN)SelectObject(mdc,sep);
        MoveToEx(mdc,CV_LINENO_W,0,NULL);LineTo(mdc,CV_LINENO_W,cr.bottom);
        SelectObject(mdc,osep);DeleteObject(sep);
        HFONT font=CreateFontA(15,0,0,0,FW_NORMAL,0,0,0,DEFAULT_CHARSET,
                               OUT_DEFAULT_PRECIS,CLIP_DEFAULT_PRECIS,
                               CLEARTYPE_QUALITY,FIXED_PITCH,"Consolas");
        HFONT ofont=(HFONT)SelectObject(mdc,font);
        SetBkMode(mdc,TRANSPARENT);
        int vis=cr.bottom/CV_LINE_H+2;
        int end=g_cv_scroll+vis;
        if(end>g_cv_nlines) end=g_cv_nlines;
        char lnbuf[12];
        for(int i=g_cv_scroll;i<end;i++){
            int y=(i-g_cv_scroll)*CV_LINE_H+1;
            sprintf(lnbuf,"%d",i+1);
            SetTextColor(mdc,RGB(90,90,90));
            RECT nr={2,y,CV_LINENO_W-6,y+CV_LINE_H};
            DrawTextA(mdc,lnbuf,-1,&nr,DT_RIGHT|DT_TOP|DT_SINGLELINE);
            if(g_cv_lines&&i<g_cv_nlines){
                SetTextColor(mdc,RGB(212,212,212));
                TextOutW(mdc,CV_LINENO_W+6,y,g_cv_lines[i],(int)wcslen(g_cv_lines[i]));
            }
        }
        SelectObject(mdc,ofont);DeleteObject(font);
        BitBlt(hdc,0,0,cr.right,cr.bottom,mdc,0,0,SRCCOPY);
        DeleteObject(bmp);DeleteDC(mdc);
        EndPaint(hwnd,&ps);
        return 0;
    }
    case WM_SIZE:{
        RECT cr;GetClientRect(hwnd,&cr);
        int vis=cr.bottom/CV_LINE_H;
        SCROLLINFO si={sizeof(si),SIF_RANGE|SIF_PAGE,0,
                       g_cv_nlines>0?g_cv_nlines-1:0,(UINT)vis,0,0};
        SetScrollInfo(hwnd,SB_VERT,&si,TRUE);
        return 0;
    }
    case WM_VSCROLL:{
        SCROLLINFO si={sizeof(si),SIF_ALL};
        GetScrollInfo(hwnd,SB_VERT,&si);
        int pos=si.nPos;
        switch(LOWORD(wp)){
        case SB_TOP:        pos=0;break;
        case SB_BOTTOM:     pos=si.nMax;break;
        case SB_LINEUP:     pos--;break;
        case SB_LINEDOWN:   pos++;break;
        case SB_PAGEUP:     pos-=(int)si.nPage;break;
        case SB_PAGEDOWN:   pos+=(int)si.nPage;break;
        case SB_THUMBTRACK: pos=si.nTrackPos;break;
        }
        if(pos<0)pos=0;if(pos>si.nMax)pos=si.nMax;
        g_cv_scroll=pos;
        si.fMask=SIF_POS;si.nPos=pos;
        SetScrollInfo(hwnd,SB_VERT,&si,TRUE);
        InvalidateRect(hwnd,NULL,FALSE);
        return 0;
    }
    case WM_MOUSEWHEEL:{
        int lines=(GET_WHEEL_DELTA_WPARAM(wp)>0)?-3:3;
        g_cv_scroll+=lines;
        if(g_cv_scroll<0)g_cv_scroll=0;
        int maxs=g_cv_nlines-1;if(maxs<0)maxs=0;
        if(g_cv_scroll>maxs)g_cv_scroll=maxs;
        SCROLLINFO si={sizeof(si),SIF_POS,0,0,0,g_cv_scroll,0};
        SetScrollInfo(hwnd,SB_VERT,&si,TRUE);
        InvalidateRect(hwnd,NULL,FALSE);
        return 0;
    }
    }
    return DefWindowProcW(hwnd,msg,wp,lp);
}

static void np_free(void)
{
    if(!g_np_lines) return;
    for(int i=0;i<g_np_nlines;i++) free(g_np_lines[i]);
    free(g_np_lines);
    g_np_lines=NULL; g_np_nlines=0;
}

static void np_load(const char *utf8)
{
    np_free();
    if(!utf8||!*utf8) return;
    int wlen=MultiByteToWideChar(CP_UTF8,0,utf8,-1,NULL,0);
    WCHAR *wide=(WCHAR*)malloc(wlen*sizeof(WCHAR));
    MultiByteToWideChar(CP_UTF8,0,utf8,-1,wide,wlen);
    int n=1;
    for(WCHAR *q=wide;*q;q++) if(*q==L'\n') n++;
    g_np_lines=(WCHAR**)malloc(n*sizeof(WCHAR*));
    g_np_nlines=0;
    WCHAR *start=wide;
    for(WCHAR *q=wide;;q++){
        if(*q==L'\n'||*q==L'\0'){
            int len=(int)(q-start);
            if(len>0&&start[len-1]==L'\r') len--;
            WCHAR *line=(WCHAR*)malloc((len+1)*sizeof(WCHAR));
            if(len) wcsncpy(line,start,len);
            line[len]=L'\0';
            g_np_lines[g_np_nlines++]=line;
            if(*q==L'\0') break;
            start=q+1;
        }
    }
    free(wide);
    g_np_scroll=0;
    if(g_np_hwnd){
        RECT cr2;GetClientRect(g_np_hwnd,&cr2);
        int code_h=cr2.bottom-NP_HEADER_H;if(code_h<1)code_h=1;
        int vis=code_h/CV_LINE_H;
        SCROLLINFO si={sizeof(si),SIF_RANGE|SIF_PAGE|SIF_POS,0,
                       g_np_nlines>0?g_np_nlines-1:0,(UINT)vis,0,0};
        SetScrollInfo(g_np_hwnd,SB_VERT,&si,TRUE);
        InvalidateRect(g_np_hwnd,NULL,TRUE);
    }
}

static void np_tex_free(void)
{
    if(g_np_tex_lines){
        for(int i=0;i<g_np_tex_nlines;i++) free(g_np_tex_lines[i]);
        free(g_np_tex_lines);
        g_np_tex_lines=NULL; g_np_tex_nlines=0;
    }
    free(g_np_tex_pixels); g_np_tex_pixels=NULL;
    g_np_tex_pw=g_np_tex_ph=g_np_tex_stride=0;
    g_np_tex_pan_y=0;
}

static void np_tex_load(const char *utf8)
{
    np_tex_free();
    if(!utf8||!*utf8) return;
    int wlen=MultiByteToWideChar(CP_UTF8,0,utf8,-1,NULL,0);
    WCHAR *wide=(WCHAR*)malloc(wlen*sizeof(WCHAR));
    MultiByteToWideChar(CP_UTF8,0,utf8,-1,wide,wlen);
    int n=1;
    for(WCHAR *q=wide;*q;q++) if(*q==L'\n') n++;
    g_np_tex_lines=(WCHAR**)malloc(n*sizeof(WCHAR*));
    g_np_tex_nlines=0;
    WCHAR *start=wide;
    for(WCHAR *q=wide;;q++){
        if(*q==L'\n'||*q==L'\0'){
            int len=(int)(q-start);
            if(len>0&&start[len-1]==L'\r') len--;
            WCHAR *line=(WCHAR*)malloc((len+1)*sizeof(WCHAR));
            if(len) wcsncpy(line,start,len);
            line[len]=L'\0';
            g_np_tex_lines[g_np_tex_nlines++]=line;
            if(*q==L'\0') break;
            start=q+1;
        }
    }
    free(wide);
    g_np_tex_scroll=0;
}

static int np_tex_load_pdf(void)
{
    if(!g_np_pdf_path[0]||!g_pdfium.initialized) return 0;
    FPDF_DOCUMENT doc=g_pdfium.LoadDocument(g_np_pdf_path,NULL);
    if(!doc) return 0;
    if(g_pdfium.GetPageCount(doc)<1){g_pdfium.CloseDocument(doc);return 0;}
    FPDF_PAGE page=g_pdfium.LoadPage(doc,0);
    if(!page){g_pdfium.CloseDocument(doc);return 0;}
    double scale=1.33; /* 96 dpi — fixed font size regardless of panel width */
    int w=(int)(g_pdfium.GetPageWidth(page)*scale+0.5); if(w<1)w=1;
    int h=(int)(g_pdfium.GetPageHeight(page)*scale+0.5); if(h<1)h=1;
    FPDF_BITMAP bm=g_pdfium.Bitmap_Create(w,h,0);
    if(!bm){g_pdfium.ClosePage(page);g_pdfium.CloseDocument(doc);return 0;}
    g_pdfium.Bitmap_FillRect(bm,0,0,w,h,0xFFFFFFFF);
    g_pdfium.RenderPageBitmap(bm,page,0,0,w,h,0,FPDF_ANNOT);
    int ss=g_pdfium.Bitmap_GetStride(bm);
    void *src=g_pdfium.Bitmap_GetBuffer(bm);
    if(!src||ss<=0){g_pdfium.Bitmap_Destroy(bm);g_pdfium.ClosePage(page);g_pdfium.CloseDocument(doc);return 0;}
    int tight=w*4;
    free(g_np_tex_pixels);
    g_np_tex_pixels=(unsigned char*)malloc((size_t)tight*h);
    if(!g_np_tex_pixels){g_pdfium.Bitmap_Destroy(bm);g_pdfium.ClosePage(page);g_pdfium.CloseDocument(doc);return 0;}
    /* Invert RGB so white pdflatex output becomes dark-themed */
    for(int row=0;row<h;row++){
        unsigned char *s=(unsigned char*)src+(size_t)row*ss;
        unsigned char *d=g_np_tex_pixels+(size_t)row*tight;
        for(int x=0;x<w;x++){
            d[x*4+0]=(unsigned char)(255-s[x*4+0]);
            d[x*4+1]=(unsigned char)(255-s[x*4+1]);
            d[x*4+2]=(unsigned char)(255-s[x*4+2]);
            d[x*4+3]=0xFF;
        }
    }
    g_np_tex_pw=w; g_np_tex_ph=h; g_np_tex_stride=tight; g_np_tex_pan_y=0;
    g_pdfium.Bitmap_Destroy(bm); g_pdfium.ClosePage(page); g_pdfium.CloseDocument(doc);
    return 1;
}

/* Count visual rows when lines wrap at mc chars per row */
static int np_vis_rows(WCHAR **lines,int n,int mc)
{
    if(mc<1)mc=1; int t=0;
    for(int i=0;i<n;i++){int l=(int)wcslen(lines[i]);t+=l==0?1:(l+mc-1)/mc;}
    return t;
}

/* Map visual row vr -> original line index *ol and char offset *os */
static void np_vis_to_src(WCHAR **lines,int n,int mc,int vr,int *ol,int *os)
{
    if(mc<1)mc=1; int row=0;
    for(int i=0;i<n;i++){
        int l=(int)wcslen(lines[i]);
        int chunks=l==0?1:(l+mc-1)/mc;
        if(vr<row+chunks){*ol=i;*os=(vr-row)*mc;return;}
        row+=chunks;
    }
    *ol=n>0?n-1:0;*os=0;
}

static LRESULT CALLBACK NodePanelWndProc(HWND hwnd,UINT msg,WPARAM wp,LPARAM lp)
{
    switch(msg){
    case WM_PAINT:{
        PAINTSTRUCT ps;HDC hdc=BeginPaint(hwnd,&ps);
        RECT cr;GetClientRect(hwnd,&cr);
        HDC mdc=CreateCompatibleDC(hdc);
        HBITMAP bmp=CreateCompatibleBitmap(hdc,cr.right,cr.bottom);
        SelectObject(mdc,bmp);

        /* Compute split geometry */
        int code_h=cr.bottom-NP_HEADER_H;
        int lean_h=(code_h-NP_DIV_H)/2;
        int div_y =NP_HEADER_H+lean_h;
        int tex_y =div_y+NP_DIV_H;

        /* ---- Header ---- */
        RECT hdr={0,0,cr.right,NP_HEADER_H};
        HBRUSH hbr=CreateSolidBrush(RGB(32,34,50));FillRect(mdc,&hdr,hbr);DeleteObject(hbr);
        HPEN lp2=CreatePen(PS_SOLID,1,RGB(55,60,90));
        HPEN olp=(HPEN)SelectObject(mdc,lp2);
        MoveToEx(mdc,0,NP_HEADER_H-1,NULL);LineTo(mdc,cr.right,NP_HEADER_H-1);
        SelectObject(mdc,olp);DeleteObject(lp2);
        /* Kind badge */
        int bx=12,by=(NP_HEADER_H-10)/2;
        HBRUSH kb=CreateSolidBrush(KIND_COL[g_np_kind]);
        HPEN   kp=CreatePen(PS_SOLID,0,KIND_COL[g_np_kind]);
        SelectObject(mdc,kb);SelectObject(mdc,kp);
        RoundRect(mdc,bx,by,bx+10,by+10,3,3);
        DeleteObject(kb);DeleteObject(kp);
        HFONT nfont=CreateFontA(13,0,0,0,FW_NORMAL,0,0,0,DEFAULT_CHARSET,
                                OUT_DEFAULT_PRECIS,CLIP_DEFAULT_PRECIS,
                                CLEARTYPE_QUALITY,DEFAULT_PITCH,"Segoe UI");
        HFONT onf=(HFONT)SelectObject(mdc,nfont);
        SetTextColor(mdc,RGB(230,230,240));SetBkMode(mdc,TRANSPARENT);
        RECT tnr={bx+16,0,cr.right-30,NP_HEADER_H};
        DrawTextA(mdc,g_np_name,-1,&tnr,DT_LEFT|DT_VCENTER|DT_SINGLELINE|DT_END_ELLIPSIS);
        int cx2=cr.right-24,cy2=4;
        g_np_close_rect=(RECT){cx2,cy2,cx2+20,cy2+20};
        SetTextColor(mdc,RGB(160,165,195));
        RECT xr={cx2,cy2,cx2+20,cy2+20};
        DrawTextA(mdc,"x",-1,&xr,DT_CENTER|DT_VCENTER|DT_SINGLELINE);
        SelectObject(mdc,onf);DeleteObject(nfont);

        /* Helper macro: draw a code section (gutter + numbered lines) */
        /* We use inline code for each section to avoid nested function issues */
        HFONT cfont=CreateFontA(15,0,0,0,FW_NORMAL,0,0,0,DEFAULT_CHARSET,
                                OUT_DEFAULT_PRECIS,CLIP_DEFAULT_PRECIS,
                                CLEARTYPE_QUALITY,FIXED_PITCH,"Consolas");
        HFONT ocf=(HFONT)SelectObject(mdc,cfont);
        SetBkMode(mdc,TRANSPARENT);

        /* ---- Lean source section (NP_HEADER_H .. div_y) ---- */
        {
            RECT sec={0,NP_HEADER_H,cr.right,div_y};
            HBRUSH sb2=CreateSolidBrush(RGB(30,30,30));FillRect(mdc,&sec,sb2);DeleteObject(sb2);
            RECT gut={0,NP_HEADER_H,CV_LINENO_W,div_y};
            HBRUSH gb2=CreateSolidBrush(RGB(24,24,24));FillRect(mdc,&gut,gb2);DeleteObject(gb2);
            HPEN gs=CreatePen(PS_SOLID,1,RGB(50,50,50));
            HPEN ogs=(HPEN)SelectObject(mdc,gs);
            MoveToEx(mdc,CV_LINENO_W,NP_HEADER_H,NULL);LineTo(mdc,CV_LINENO_W,div_y);
            SelectObject(mdc,ogs);DeleteObject(gs);
            IntersectClipRect(mdc,0,NP_HEADER_H,cr.right,div_y);
            /* Compute wrapping */
            SIZE csz;GetTextExtentPoint32A(mdc,"W",1,&csz);
            int cw=csz.cx;if(cw<1)cw=1;g_np_char_w=cw;
            int avail=cr.right-CV_LINENO_W-12;if(avail<cw)avail=cw;
            int mc=avail/cw;
            int tot_vis=g_np_lines?np_vis_rows(g_np_lines,g_np_nlines,mc):0;
            int vis_cnt=lean_h/CV_LINE_H+2;
            char lnbuf[12];
            for(int vr=g_np_scroll;vr<g_np_scroll+vis_cnt&&vr<tot_vis;vr++){
                int src_l=0,src_s=0;
                if(g_np_lines) np_vis_to_src(g_np_lines,g_np_nlines,mc,vr,&src_l,&src_s);
                int y=NP_HEADER_H+(vr-g_np_scroll)*CV_LINE_H+1;
                if(y>=div_y)break;
                if(src_s==0){
                    sprintf(lnbuf,"%d",src_l+1);
                    SetTextColor(mdc,RGB(90,90,90));
                    RECT lnr={2,y,CV_LINENO_W-6,y+CV_LINE_H};
                    DrawTextA(mdc,lnbuf,-1,&lnr,DT_RIGHT|DT_TOP|DT_SINGLELINE);
                }
                if(g_np_lines&&src_l<g_np_nlines){
                    int src_len=(int)wcslen(g_np_lines[src_l]);
                    int chunk=src_len-src_s;if(chunk>mc)chunk=mc;
                    if(chunk>0){
                        SetTextColor(mdc,RGB(212,212,212));
                        TextOutW(mdc,CV_LINENO_W+6,y,g_np_lines[src_l]+src_s,chunk);
                    }
                }
            }
            SelectClipRgn(mdc,NULL);
        }

        /* ---- Divider bar (div_y .. tex_y) ---- */
        {
            RECT div_rc={0,div_y,cr.right,tex_y};
            HBRUSH db=CreateSolidBrush(RGB(28,30,46));FillRect(mdc,&div_rc,db);DeleteObject(db);
            HPEN dp=CreatePen(PS_SOLID,1,RGB(50,54,80));
            HPEN odp=(HPEN)SelectObject(mdc,dp);
            MoveToEx(mdc,0,div_y,NULL);LineTo(mdc,cr.right,div_y);
            MoveToEx(mdc,0,tex_y-1,NULL);LineTo(mdc,cr.right,tex_y-1);
            SelectObject(mdc,odp);DeleteObject(dp);
            HFONT df=CreateFontA(11,0,0,0,FW_NORMAL,0,0,0,DEFAULT_CHARSET,
                                 OUT_DEFAULT_PRECIS,CLIP_DEFAULT_PRECIS,
                                 CLEARTYPE_QUALITY,DEFAULT_PITCH,"Segoe UI");
            HFONT odf=(HFONT)SelectObject(mdc,df);
            SetTextColor(mdc,RGB(100,105,135));SetBkMode(mdc,TRANSPARENT);
            RECT dl={8,div_y,cr.right-8,tex_y};
            DrawTextA(mdc,"Mathematical Form",-1,&dl,DT_LEFT|DT_VCENTER|DT_SINGLELINE);
            SelectObject(mdc,odf);DeleteObject(df);
        }

        /* ---- LaTeX section (tex_y .. cr.bottom) ---- */
        {
            RECT sec={0,tex_y,cr.right,cr.bottom};
            HBRUSH sb3=CreateSolidBrush(RGB(30,30,30));FillRect(mdc,&sec,sb3);DeleteObject(sb3);
            IntersectClipRect(mdc,0,tex_y,cr.right,cr.bottom);
            if(g_np_tex_state==1){
                /* Converting... */
                SetTextColor(mdc,RGB(100,105,135));SetBkMode(mdc,TRANSPARENT);
                RECT ml={CV_LINENO_W+6,tex_y,cr.right,cr.bottom};
                DrawTextA(mdc,"Converting...",-1,&ml,DT_LEFT|DT_TOP|DT_SINGLELINE);
            } else if(g_np_tex_state==3){
                SetTextColor(mdc,RGB(160,80,80));SetBkMode(mdc,TRANSPARENT);
                RECT ml={CV_LINENO_W+6,tex_y,cr.right,cr.bottom};
                DrawTextA(mdc,"Conversion failed",-1,&ml,DT_LEFT|DT_TOP|DT_SINGLELINE);
            } else if(g_np_tex_state==2){
                if(g_np_tex_pixels&&g_np_tex_pw>0){
                    /* Rendered PDF bitmap: 1:1 native pixels, pan vertically */
                    BITMAPINFO bi2; ZeroMemory(&bi2,sizeof(bi2));
                    bi2.bmiHeader.biSize=sizeof(BITMAPINFOHEADER);
                    bi2.bmiHeader.biWidth=g_np_tex_pw;
                    bi2.bmiHeader.biHeight=-g_np_tex_ph;
                    bi2.bmiHeader.biPlanes=1;
                    bi2.bmiHeader.biBitCount=32;
                    bi2.bmiHeader.biCompression=BI_RGB;
                    StretchDIBits(mdc,0,tex_y-g_np_tex_pan_y,g_np_tex_pw,g_np_tex_ph,
                                  0,0,g_np_tex_pw,g_np_tex_ph,
                                  g_np_tex_pixels,&bi2,DIB_RGB_COLORS,SRCCOPY);
                } else if(g_np_tex_lines){
                    RECT gut={0,tex_y,CV_LINENO_W,cr.bottom};
                    HBRUSH gb3=CreateSolidBrush(RGB(24,24,24));FillRect(mdc,&gut,gb3);DeleteObject(gb3);
                    HPEN gs2=CreatePen(PS_SOLID,1,RGB(50,50,50));
                    HPEN ogs2=(HPEN)SelectObject(mdc,gs2);
                    MoveToEx(mdc,CV_LINENO_W,tex_y,NULL);LineTo(mdc,CV_LINENO_W,cr.bottom);
                    SelectObject(mdc,ogs2);DeleteObject(gs2);
                    int avail2=cr.right-CV_LINENO_W-12;if(avail2<g_np_char_w)avail2=g_np_char_w;
                    int mc2=g_np_char_w>0?avail2/g_np_char_w:40;if(mc2<1)mc2=1;
                    int tot2=np_vis_rows(g_np_tex_lines,g_np_tex_nlines,mc2);
                    int tex_h2=cr.bottom-tex_y;
                    int vis2=tex_h2/CV_LINE_H+2;
                    char lnbuf2[12];
                    for(int vr=g_np_tex_scroll;vr<g_np_tex_scroll+vis2&&vr<tot2;vr++){
                        int tl=0,ts=0;
                        np_vis_to_src(g_np_tex_lines,g_np_tex_nlines,mc2,vr,&tl,&ts);
                        int y=tex_y+(vr-g_np_tex_scroll)*CV_LINE_H+1;
                        if(y>=cr.bottom)break;
                        if(ts==0){
                            sprintf(lnbuf2,"%d",tl+1);
                            SetTextColor(mdc,RGB(90,90,90));
                            RECT lnr2={2,y,CV_LINENO_W-6,y+CV_LINE_H};
                            DrawTextA(mdc,lnbuf2,-1,&lnr2,DT_RIGHT|DT_TOP|DT_SINGLELINE);
                        }
                        int tlen=(int)wcslen(g_np_tex_lines[tl]);
                        int chunk2=tlen-ts;if(chunk2>mc2)chunk2=mc2;
                        if(chunk2>0){
                            SetTextColor(mdc,RGB(200,212,180));
                            TextOutW(mdc,CV_LINENO_W+6,y,g_np_tex_lines[tl]+ts,chunk2);
                        }
                    }
                }
            }
            SelectClipRgn(mdc,NULL);
        }

        SelectObject(mdc,ocf);DeleteObject(cfont);
        /* Resize grip: 4px strip on the left edge */
        RECT rh={0,0,4,cr.bottom};
        HBRUSH rhb=CreateSolidBrush(RGB(55,60,100));FillRect(mdc,&rh,rhb);DeleteObject(rhb);
        BitBlt(hdc,0,0,cr.right,cr.bottom,mdc,0,0,SRCCOPY);
        DeleteObject(bmp);DeleteDC(mdc);
        EndPaint(hwnd,&ps);
        return 0;
    }
    case WM_SETCURSOR:{
        POINT cur;GetCursorPos(&cur);ScreenToClient(hwnd,&cur);
        if(cur.x>=0&&cur.x<6){SetCursor(LoadCursor(NULL,IDC_SIZEWE));return TRUE;}
        break;
    }
    case WM_LBUTTONDOWN:{
        int mx2=GET_X_LPARAM(lp),my2=GET_Y_LPARAM(lp);
        if(mx2<6){
            RECT wr;GetWindowRect(hwnd,&wr);
            g_np_resize_start_w=wr.right-wr.left;
            POINT sp={mx2,my2};ClientToScreen(hwnd,&sp);
            g_np_resize_start_x=sp.x;
            g_np_resizing=TRUE;SetCapture(hwnd);
            return 0;
        }
        if(mx2>=g_np_close_rect.left&&mx2<g_np_close_rect.right&&
           my2>=g_np_close_rect.top&&my2<g_np_close_rect.bottom){
            g_sel_node=-1;
            ShowWindow(hwnd,SW_HIDE);
            InvalidateRect(GetParent(hwnd),NULL,TRUE);
        }
        return 0;
    }
    case WM_MOUSEMOVE:{
        if(g_np_resizing){
            POINT sp={GET_X_LPARAM(lp),0};ClientToScreen(hwnd,&sp);
            int new_w=g_np_resize_start_w+(g_np_resize_start_x-sp.x);
            if(new_w<150)new_w=150;if(new_w>1400)new_w=1400;
            g_np_panel_w=new_w;
            HWND par=GetParent(hwnd);RECT pcr;GetClientRect(par,&pcr);
            MoveWindow(hwnd,pcr.right-new_w,0,new_w,pcr.bottom,TRUE);
        }
        return 0;
    }
    case WM_LBUTTONUP:
        if(g_np_resizing){g_np_resizing=FALSE;ReleaseCapture();}
        return 0;
    case WM_SIZE:{
        RECT cr;GetClientRect(hwnd,&cr);
        int code_h2=cr.bottom-NP_HEADER_H;if(code_h2<1)code_h2=1;
        int lean_h2=(code_h2-NP_DIV_H)/2;if(lean_h2<1)lean_h2=1;
        int vis=lean_h2/CV_LINE_H;
        int avail_s=cr.right-CV_LINENO_W-12;if(avail_s<g_np_char_w)avail_s=g_np_char_w;
        int mc_s=g_np_char_w>0?avail_s/g_np_char_w:999;if(mc_s<1)mc_s=1;
        int tot_s=g_np_lines?np_vis_rows(g_np_lines,g_np_nlines,mc_s):0;
        SCROLLINFO si={sizeof(si),SIF_RANGE|SIF_PAGE,0,
                       tot_s>0?tot_s-1:0,(UINT)vis,0,0};
        SetScrollInfo(hwnd,SB_VERT,&si,TRUE);
        return 0;
    }
    case WM_VSCROLL:{
        SCROLLINFO si={sizeof(si),SIF_ALL};
        GetScrollInfo(hwnd,SB_VERT,&si);
        int pos=si.nPos;
        switch(LOWORD(wp)){
        case SB_TOP:        pos=0;break;
        case SB_BOTTOM:     pos=si.nMax;break;
        case SB_LINEUP:     pos--;break;
        case SB_LINEDOWN:   pos++;break;
        case SB_PAGEUP:     pos-=(int)si.nPage;break;
        case SB_PAGEDOWN:   pos+=(int)si.nPage;break;
        case SB_THUMBTRACK: pos=si.nTrackPos;break;
        }
        if(pos<0)pos=0;if(pos>si.nMax)pos=si.nMax;
        g_np_scroll=pos;
        si.fMask=SIF_POS;si.nPos=pos;
        SetScrollInfo(hwnd,SB_VERT,&si,TRUE);
        InvalidateRect(hwnd,NULL,FALSE);
        return 0;
    }
    case WM_MOUSEWHEEL:{
        POINT pt3={GET_X_LPARAM(lp),GET_Y_LPARAM(lp)};
        ScreenToClient(hwnd,&pt3);
        RECT cr3;GetClientRect(hwnd,&cr3);
        int code_h3=cr3.bottom-NP_HEADER_H;
        int lean_h3=(code_h3-NP_DIV_H)/2;
        int div_y3=NP_HEADER_H+lean_h3;
        int lines=(GET_WHEEL_DELTA_WPARAM(wp)>0)?-3:3;
        if(pt3.y<div_y3){
            g_np_scroll+=lines;
            if(g_np_scroll<0)g_np_scroll=0;
            {int avail_w3=cr3.right-CV_LINENO_W-12;if(avail_w3<g_np_char_w)avail_w3=g_np_char_w;
             int mc3=g_np_char_w>0?avail_w3/g_np_char_w:999;if(mc3<1)mc3=1;
             int tot3=g_np_lines?np_vis_rows(g_np_lines,g_np_nlines,mc3):0;
             int maxs=tot3-1;if(maxs<0)maxs=0;
             if(g_np_scroll>maxs)g_np_scroll=maxs;}
            SCROLLINFO si={sizeof(si),SIF_POS,0,0,0,g_np_scroll,0};
            SetScrollInfo(hwnd,SB_VERT,&si,TRUE);
        } else {
            if(g_np_tex_pixels&&g_np_tex_pw>0){
                int sec_w=cr3.right;
                int disp_h=(int)((double)g_np_tex_ph*sec_w/g_np_tex_pw+0.5);
                int sec_h=cr3.bottom-(div_y3+NP_DIV_H);
                int delta=(GET_WHEEL_DELTA_WPARAM(wp)>0)?-60:60;
                g_np_tex_pan_y+=delta;
                if(g_np_tex_pan_y<0)g_np_tex_pan_y=0;
                int max_pan=disp_h-sec_h;if(max_pan<0)max_pan=0;
                if(g_np_tex_pan_y>max_pan)g_np_tex_pan_y=max_pan;
            } else {
                g_np_tex_scroll+=lines;
                if(g_np_tex_scroll<0)g_np_tex_scroll=0;
                int maxs=g_np_tex_nlines-1;if(maxs<0)maxs=0;
                if(g_np_tex_scroll>maxs)g_np_tex_scroll=maxs;
            }
        }
        InvalidateRect(hwnd,NULL,FALSE);
        return 0;
    }
    }
    return DefWindowProcW(hwnd,msg,wp,lp);
}

/* ================================================================
   Close file helpers
   ================================================================ */

static void close_lean(HWND hwnd, int idx)
{
    free(g_lean[idx].text);
    memmove(&g_lean[idx],&g_lean[idx+1],(g_nlean-idx-1)*sizeof(LeanDoc));
    g_nlean--;
    memset(&g_lean[g_nlean],0,sizeof(LeanDoc));
    for(int j=0;j<g_npdf;j++){
        if(g_pdf[j].lean_idx==idx)       g_pdf[j].lean_idx=-1;
        else if(g_pdf[j].lean_idx>idx)   g_pdf[j].lean_idx--;
    }
    if(g_sel_kind==SEL_LEAN){
        if(g_sel_idx==idx){
            g_sel_kind=SEL_NONE;g_sel_idx=-1;
            ShowWindow(g_cv_hwnd,SW_HIDE);
            if(g_sel_node>=0){g_sel_node=-1;if(g_np_hwnd)ShowWindow(g_np_hwnd,SW_HIDE);}
        }
        else if(g_sel_idx>idx) g_sel_idx--;
    }
    InvalidateRect(hwnd,NULL,TRUE);
}

static void close_pdf(HWND hwnd, int idx)
{
    pdf_close(&g_pdf[idx]);
    memmove(&g_pdf[idx],&g_pdf[idx+1],(g_npdf-idx-1)*sizeof(PdfDoc));
    g_npdf--;
    memset(&g_pdf[g_npdf],0,sizeof(PdfDoc));
    if(g_sel_kind==SEL_PDF){
        if(g_sel_idx==idx){g_sel_kind=SEL_NONE;g_sel_idx=-1;}
        else if(g_sel_idx>idx) g_sel_idx--;
    }
    InvalidateRect(hwnd,NULL,TRUE);
}

static void close_node_panel(HWND hwnd)
{
    if(g_np_conv_proc!=INVALID_HANDLE_VALUE){
        TerminateProcess(g_np_conv_proc,1);CloseHandle(g_np_conv_proc);
        g_np_conv_proc=INVALID_HANDLE_VALUE;
    }
    KillTimer(hwnd,IDT_CONV_POLL);
    np_tex_free(); g_np_tex_state=0;
    g_sel_node=-1;
    if(g_np_hwnd) ShowWindow(g_np_hwnd,SW_HIDE);
    InvalidateRect(hwnd,NULL,TRUE);
}

static void get_exe_directory(char *dir, size_t dir_size); /* forward decl */

static void open_node_panel(HWND hwnd, LeanDoc *doc, int node_idx)
{
    /* Cancel any running conversion */
    if(g_np_conv_proc!=INVALID_HANDLE_VALUE){
        TerminateProcess(g_np_conv_proc,1);CloseHandle(g_np_conv_proc);
        g_np_conv_proc=INVALID_HANDLE_VALUE;
    }
    KillTimer(hwnd,IDT_CONV_POLL);
    np_tex_free(); g_np_tex_scroll=0; g_np_tex_state=0;

    g_sel_node=node_idx;
    strncpy(g_np_name,doc->nd[node_idx].name,NAME_LEN-1);
    g_np_kind=doc->nd[node_idx].kind;
    char *src=extract_node_source(doc,node_idx);
    const char *lean_src=src?src:"(source not available)";
    np_load(lean_src);

    /* Write lean snippet to temp file */
    char tmp_dir[MAX_PATH];
    GetTempPathA(MAX_PATH,tmp_dir);
    snprintf(g_np_lean_path,MAX_PATH,"%spv_lean_in.txt",tmp_dir);
    snprintf(g_np_tex_path, MAX_PATH,"%spv_lean_out.tex",tmp_dir);
    snprintf(g_np_pdf_path, MAX_PATH,"%spv_lean_out.pdf",tmp_dir);
    FILE *tf=fopen(g_np_lean_path,"w");
    if(tf){fputs(lean_src,tf);fclose(tf);}
    free(src);

    /* Locate script and launch */
    char exe_dir[MAX_PATH],script[MAX_PATH],cmd[4096];
    get_exe_directory(exe_dir,sizeof(exe_dir));
    snprintf(script,sizeof(script),"%s\\lean_to_latex.py",exe_dir);
    if(GetFileAttributesA(script)!=INVALID_FILE_ATTRIBUTES){
        snprintf(cmd,sizeof(cmd),
            "cmd.exe /C py -3 \"%s\" \"%s\" \"%s\" || python \"%s\" \"%s\" \"%s\"",
            script,g_np_lean_path,g_np_tex_path,
            script,g_np_lean_path,g_np_tex_path);
        STARTUPINFOA si2={0};si2.cb=sizeof(si2);
        PROCESS_INFORMATION pi2={0};
        if(CreateProcessA(NULL,cmd,NULL,NULL,FALSE,CREATE_NO_WINDOW,NULL,NULL,&si2,&pi2)){
            g_np_conv_proc=pi2.hProcess;CloseHandle(pi2.hThread);
            g_np_tex_state=1;
            SetTimer(hwnd,IDT_CONV_POLL,500,NULL);
        } else {
            g_np_tex_state=3;
        }
    }

    if(!g_np_hwnd) return;
    RECT cr;GetClientRect(hwnd,&cr);
    int pw=g_np_panel_w;
    int max_pw=cr.right-SW()-40;if(pw>max_pw)pw=max_pw;
    if(pw<100)pw=100;
    MoveWindow(g_np_hwnd,cr.right-pw,0,pw,cr.bottom,TRUE);
    ShowWindow(g_np_hwnd,SW_SHOW);
    InvalidateRect(g_np_hwnd,NULL,TRUE);
    InvalidateRect(hwnd,NULL,FALSE);
}

/* ================================================================
   Selection
   ================================================================ */

static void select_lean(HWND hwnd, int idx)
{
    if(g_sel_node>=0) close_node_panel(hwnd);
    g_sel_kind=SEL_LEAN;g_sel_idx=idx;
    LeanDoc *doc=&g_lean[idx];
    if(doc->view_mode==VIEW_TEXT){
        code_view_load(doc->text?doc->text:"");
        ShowWindow(g_cv_hwnd,SW_SHOW);
    } else {
        ShowWindow(g_cv_hwnd,SW_HIDE);
    }
    InvalidateRect(hwnd,NULL,TRUE);
}

static void select_pdf(HWND hwnd, int idx)
{
    if(g_sel_node>=0) close_node_panel(hwnd);
    g_sel_kind=SEL_PDF;g_sel_idx=idx;
    ShowWindow(g_cv_hwnd,SW_HIDE);
    InvalidateRect(hwnd,NULL,TRUE);
}

/* ================================================================
   File open / convert
   ================================================================ */

static void open_lean_file(HWND hwnd)
{
    OPENFILENAMEA ofn={0};char fn[MAX_PATH]={0};
    ofn.lStructSize=sizeof(ofn);ofn.hwndOwner=hwnd;
    ofn.lpstrFilter="Lean Files\0*.lean\0All Files\0*.*\0";
    ofn.lpstrFile=fn;ofn.nMaxFile=MAX_PATH;
    ofn.Flags=OFN_FILEMUSTEXIST|OFN_PATHMUSTEXIST;
    if(!GetOpenFileNameA(&ofn))return;
    if(!has_ext(fn,".lean")){MessageBoxA(hwnd,"Please choose a .lean file.","Unsupported",MB_ICONWARNING);return;}
    int idx=lean_open(hwnd,fn);
    if(idx>=0)select_lean(hwnd,idx);
}

static void open_pdf_file(HWND hwnd)
{
    OPENFILENAMEA ofn={0};char fn[MAX_PATH]={0};
    ofn.lStructSize=sizeof(ofn);ofn.hwndOwner=hwnd;
    ofn.lpstrFilter="PDF Files\0*.pdf\0All Files\0*.*\0";
    ofn.lpstrFile=fn;ofn.nMaxFile=MAX_PATH;
    ofn.Flags=OFN_FILEMUSTEXIST|OFN_PATHMUSTEXIST;
    if(!GetOpenFileNameA(&ofn))return;
    if(!has_ext(fn,".pdf")){MessageBoxA(hwnd,"Please choose a .pdf file.","Unsupported",MB_ICONWARNING);return;}
    int idx=pdf_open_doc(hwnd,fn);
    if(idx>=0)select_pdf(hwnd,idx);
}

static void make_converted_lean_path(const char *pdf_path,char *out,size_t out_size)
{
    strncpy(out,pdf_path,out_size-1);out[out_size-1]='\0';
    char *s1=strrchr(out,'\\'),*s2=strrchr(out,'/');
    char *slash=(s1>s2)?s1:s2;
    char *dot=strrchr(out,'.');
    if(!dot||(slash&&dot<slash))strncat(out,"_converted.lean",out_size-strlen(out)-1);
    else{*dot='\0';strncat(out,"_converted.lean",out_size-strlen(out)-1);}
}

static void get_exe_directory(char *dir,size_t dir_size)
{
    DWORD n=GetModuleFileNameA(NULL,dir,(DWORD)dir_size);
    if(!n||n>=dir_size){strncpy(dir,".",dir_size-1);dir[dir_size-1]='\0';return;}
    char *s1=strrchr(dir,'\\'),*s2=strrchr(dir,'/');
    char *slash=(s1>s2)?s1:s2;if(slash)*slash='\0';
}

static int run_command_wait(HWND hwnd,const char *cmdline,DWORD *exit_code)
{
    STARTUPINFOA si;PROCESS_INFORMATION pi;char cmd[4096];
    ZeroMemory(&si,sizeof(si));ZeroMemory(&pi,sizeof(pi));si.cb=sizeof(si);
    strncpy(cmd,cmdline,sizeof(cmd)-1);cmd[sizeof(cmd)-1]='\0';
    if(!CreateProcessA(NULL,cmd,NULL,NULL,FALSE,CREATE_NEW_CONSOLE,NULL,NULL,&si,&pi)){
        char msg[512];snprintf(msg,sizeof(msg),"Could not start script.\n\nError: %lu",GetLastError());
        MessageBoxA(hwnd,msg,"Convert Paper",MB_ICONERROR);return 0;
    }
    WaitForSingleObject(pi.hProcess,INFINITE);
    if(exit_code)GetExitCodeProcess(pi.hProcess,exit_code);
    CloseHandle(pi.hProcess);CloseHandle(pi.hThread);return 1;
}

static void convert_current_pdf(HWND hwnd)
{
    if(g_sel_kind!=SEL_PDF){
        MessageBoxA(hwnd,"Select a PDF in the sidebar first.","No PDF selected",MB_ICONINFORMATION);
        return;
    }
    PdfDoc *pdf=&g_pdf[g_sel_idx];
    char exe_dir[MAX_PATH],script[MAX_PATH],out_lean[MAX_PATH],cmd[4096];
    DWORD exit_code=1;
    get_exe_directory(exe_dir,sizeof(exe_dir));
    snprintf(script,sizeof(script),"%s\\convert_paper.py",exe_dir);
    make_converted_lean_path(pdf->path,out_lean,sizeof(out_lean));
    if(GetFileAttributesA(script)==INVALID_FILE_ATTRIBUTES){
        char msg[1024];snprintf(msg,sizeof(msg),"Cannot find:\n\n%s\n\nPut convert_paper.py next to proof_viz.exe.",script);
        MessageBoxA(hwnd,msg,"Convert Paper",MB_ICONERROR);return;
    }
    snprintf(cmd,sizeof(cmd),"cmd.exe /C py -3 \"%s\" \"%s\" \"%s\" || python \"%s\" \"%s\" \"%s\"",
             script,pdf->path,out_lean,script,pdf->path,out_lean);
    snprintf(pdf->status,INFO_LEN,"Converting...\r\n%s",pdf->basename);
    InvalidateRect(hwnd,NULL,TRUE);
    if(!run_command_wait(hwnd,cmd,&exit_code))return;
    if(exit_code!=0){
        char msg[256];snprintf(msg,sizeof(msg),"Script exited with code %lu.",exit_code);
        MessageBoxA(hwnd,msg,"Convert Paper failed",MB_ICONERROR);return;
    }
    if(GetFileAttributesA(out_lean)==INVALID_FILE_ATTRIBUTES){
        MessageBoxA(hwnd,"Script finished but no .lean file was created.","Convert Paper",MB_ICONERROR);return;
    }
    int lidx=lean_open(hwnd,out_lean);
    if(lidx<0)return;
    pdf->lean_idx=lidx;  /* PDF now lives as subrow under the lean file */
    snprintf(pdf->status,INFO_LEN,"PDF: %s\r\nPage %d of %d\r\nLinked: %s",
             pdf->basename,pdf->page_index+1,pdf->page_count,g_lean[lidx].basename);
    select_lean(hwnd,lidx);
    MessageBoxA(hwnd,
        "Conversion complete.\n\nThe .lean file has been opened and this PDF has been linked to it.",
        "Convert Paper",MB_ICONINFORMATION);
}

/* ================================================================
   Window layout
   ================================================================ */

static void resize_children(HWND hwnd)
{
    RECT cr;GetClientRect(hwnd,&cr);
    int rx=SW()+1,rw=cr.right-rx;if(rw<1)rw=1;
    int vis=g_sidebar_collapsed?SW_HIDE:SW_SHOW;
    MoveWindow(g_btn_open_lean,BTN_X, 58,BTN_W,BTN_H,TRUE);
    MoveWindow(g_btn_open_pdf, BTN_X,100,BTN_W,BTN_H,TRUE);
    ShowWindow(g_btn_open_lean,vis);
    ShowWindow(g_btn_open_pdf, vis);
    MoveWindow(g_cv_hwnd,rx,TEXT_TOP_OFFSET,rw,cr.bottom-TEXT_TOP_OFFSET,TRUE);
    if(g_np_hwnd&&IsWindowVisible(g_np_hwnd)){
        int pw=NODE_PANEL_W;
        int max_pw=cr.right-rx-20;if(pw>max_pw)pw=max_pw;
        if(pw<100)pw=100;
        MoveWindow(g_np_hwnd,cr.right-pw,0,pw,cr.bottom,TRUE);
    }
}

/* ================================================================
   Hover helpers
   ================================================================ */

static BOOL pt_in_rect(int x, int y, RECT r)
{
    return x>=r.left && x<r.right && y>=r.top && y<r.bottom;
}

/* Update all overlay hover states; return TRUE if any changed */
static BOOL update_hover(int mx, int my)
{
    BOOL chg = FALSE;
#define UPD(field, cond) { BOOL nv=(cond); if(nv!=field){field=nv;chg=TRUE;} }
    UPD(g_hover_prev,    pt_in_rect(mx,my,g_ovl_prev))
    UPD(g_hover_next,    pt_in_rect(mx,my,g_ovl_next))
    UPD(g_hover_convert, pt_in_rect(mx,my,g_ovl_convert))
    UPD(g_hover_graph,   pt_in_rect(mx,my,g_ovl_graph))
    UPD(g_hover_text,    pt_in_rect(mx,my,g_ovl_text))
#undef UPD
    return chg;
}

/* ================================================================
   WndProc
   ================================================================ */

static LRESULT CALLBACK WndProc(HWND hwnd, UINT msg, WPARAM wp, LPARAM lp)
{
    switch (msg) {

    case WM_PAINT: {
        PAINTSTRUCT ps;HDC hdc=BeginPaint(hwnd,&ps);
        RECT cr;GetClientRect(hwnd,&cr);
        HDC mdc=CreateCompatibleDC(hdc);
        HBITMAP bmp=CreateCompatibleBitmap(hdc,cr.right,cr.bottom);
        SelectObject(mdc,bmp);

        /* Background */
        HBRUSH bg=CreateSolidBrush(RGB(22,22,32));FillRect(mdc,&cr,bg);DeleteObject(bg);

        HFONT font=CreateFontA(12,0,0,0,FW_NORMAL,0,0,0,DEFAULT_CHARSET,
                               OUT_DEFAULT_PRECIS,CLIP_DEFAULT_PRECIS,
                               CLEARTYPE_QUALITY,DEFAULT_PITCH,"Segoe UI");
        HFONT old_font=(HFONT)SelectObject(mdc,font);

        /* Sidebar background + divider */
        RECT sr={0,0,SW(),cr.bottom};
        HBRUSH sb=CreateSolidBrush(RGB(30,30,42));FillRect(mdc,&sr,sb);DeleteObject(sb);
        HPEN sep=CreatePen(PS_SOLID,1,RGB(55,55,70));
        HPEN old_sep=(HPEN)SelectObject(mdc,sep);
        MoveToEx(mdc,SW(),0,NULL);LineTo(mdc,SW(),cr.bottom);
        SelectObject(mdc,old_sep);DeleteObject(sep);

        /* Collapse toggle button */
        {
            int bx=SW()-22,by=14,bw=20,bh=28;
            g_sidebar_toggle_btn=(RECT){bx,by,bx+bw,by+bh};
            HBRUSH tbr=CreateSolidBrush(RGB(45,45,62));
            FillRect(mdc,&g_sidebar_toggle_btn,tbr);DeleteObject(tbr);
            SetTextColor(mdc,RGB(160,165,190));SetBkMode(mdc,TRANSPARENT);
            DrawTextA(mdc,g_sidebar_collapsed?">":"<",-1,
                      &g_sidebar_toggle_btn,DT_CENTER|DT_VCENTER|DT_SINGLELINE);
        }

        if(!g_sidebar_collapsed){
            /* Sidebar title */
            SetTextColor(mdc,RGB(235,235,245));SetBkMode(mdc,TRANSPARENT);
            RECT title={BTN_X,18,SIDEBAR_W-36,44};
            DrawTextA(mdc,"ProofViz",-1,&title,DT_LEFT|DT_VCENTER|DT_SINGLELINE);

            /* File list */
            draw_file_list(mdc,cr.bottom);

            /* Status */
            const char *status="Open a .lean or .pdf file.";
            if(g_sel_kind==SEL_LEAN&&g_sel_idx>=0) status=g_lean[g_sel_idx].status;
            else if(g_sel_kind==SEL_PDF&&g_sel_idx>=0) status=g_pdf[g_sel_idx].status;
            SetTextColor(mdc,RGB(150,155,175));SetBkMode(mdc,TRANSPARENT);
            RECT ir={BTN_X,cr.bottom-115,SIDEBAR_W-14,cr.bottom-12};
            DrawTextA(mdc,status,-1,&ir,DT_LEFT|DT_WORDBREAK);
        }

        /* Main view */
        RECT vr={SW()+1,0,cr.right,cr.bottom};

        if(g_sel_kind==SEL_LEAN&&g_sel_idx>=0) {
            LeanDoc *doc=&g_lean[g_sel_idx];
            if(doc->view_mode==VIEW_GRAPH) {
                HRGN clip=CreateRectRgn(vr.left,vr.top,vr.right,vr.bottom);
                SelectClipRgn(mdc,clip);
                if(doc->nnd>0) draw_graph(mdc,doc);
                else {
                    SetTextColor(mdc,RGB(90,90,110));SetBkMode(mdc,TRANSPARENT);
                    DrawTextA(mdc,"Open a .lean file to view its proof tree",-1,&vr,DT_CENTER|DT_VCENTER|DT_SINGLELINE);
                }
                draw_legend(mdc,vr.left+18,vr.top+18);
                SelectClipRgn(mdc,NULL);DeleteObject(clip);
            }
            /* text view handled by g_text_hwnd child control */
            /* Lean overlay: Graph / Text toggle */
            draw_lean_overlays(mdc,vr,doc->view_mode);

        } else if(g_sel_kind==SEL_PDF&&g_sel_idx>=0) {
            HRGN clip=CreateRectRgn(vr.left,vr.top,vr.right,vr.bottom);
            SelectClipRgn(mdc,clip);
            pdf_draw_page(mdc,vr,&g_pdf[g_sel_idx]);
            SelectClipRgn(mdc,NULL);DeleteObject(clip);
            /* PDF overlay: Prev / Next / Convert */
            draw_pdf_overlays(mdc,vr);
        } else {
            SetTextColor(mdc,RGB(65,65,85));SetBkMode(mdc,TRANSPARENT);
            DrawTextA(mdc,"Open a .lean or .pdf file from the sidebar",-1,&vr,DT_CENTER|DT_VCENTER|DT_SINGLELINE);
            /* reset rects so stale hits don't fire */
            memset(&g_ovl_prev,0,sizeof(RECT));
            memset(&g_ovl_next,0,sizeof(RECT));
            memset(&g_ovl_convert,0,sizeof(RECT));
            memset(&g_ovl_graph,0,sizeof(RECT));
            memset(&g_ovl_text,0,sizeof(RECT));
        }

        SelectObject(mdc,old_font);DeleteObject(font);
        BitBlt(hdc,0,0,cr.right,cr.bottom,mdc,0,0,SRCCOPY);
        DeleteObject(bmp);DeleteDC(mdc);
        EndPaint(hwnd,&ps);
        return 0;
    }

    case WM_COMMAND:
        switch(LOWORD(wp)){
        case IDC_OPEN_LEAN: open_lean_file(hwnd); return 0;
        case IDC_OPEN_PDF:  open_pdf_file(hwnd);  return 0;
        }
        break;

    case WM_SIZE: resize_children(hwnd); return 0;

    case WM_KEYDOWN:
        if(wp=='O') open_lean_file(hwnd);
        if(wp=='P') open_pdf_file(hwnd);
        if(wp=='T'&&g_sel_kind==SEL_LEAN&&g_sel_idx>=0){
            if(g_sel_node>=0) close_node_panel(hwnd);
            LeanDoc *doc=&g_lean[g_sel_idx];
            doc->view_mode=VIEW_TEXT;
            code_view_load(doc->text?doc->text:"");
            ShowWindow(g_cv_hwnd,SW_SHOW);
            InvalidateRect(hwnd,NULL,TRUE);
        }
        if(wp=='G'&&g_sel_kind==SEL_LEAN&&g_sel_idx>=0){
            g_lean[g_sel_idx].view_mode=VIEW_GRAPH;
            ShowWindow(g_cv_hwnd,SW_HIDE);
            InvalidateRect(hwnd,NULL,TRUE);
        }
        if(g_sel_kind==SEL_PDF&&g_sel_idx>=0){
            if(wp==VK_PRIOR) pdf_change_page(hwnd,&g_pdf[g_sel_idx],-1);
            if(wp==VK_NEXT)  pdf_change_page(hwnd,&g_pdf[g_sel_idx], 1);
        }
        if(wp==VK_ESCAPE) PostQuitMessage(0);
        return 0;

    case WM_MOUSEWHEEL: {
        POINT pt={GET_X_LPARAM(lp),GET_Y_LPARAM(lp)};
        ScreenToClient(hwnd,&pt);
        if(pt.x<SW())return 0;
        if(g_sel_kind==SEL_PDF&&g_sel_idx>=0){
            PdfDoc *pdf=&g_pdf[g_sel_idx];
            double oldz=pdf->zoom;
            int delta=GET_WHEEL_DELTA_WPARAM(wp);
            pdf->zoom*=(delta>0)?1.15:(1.0/1.15);
            if(pdf->zoom<0.25)pdf->zoom=0.25;
            if(pdf->zoom>5.0) pdf->zoom=5.0;
            pdf_render_page(hwnd,pdf);
            pdf->pan_y=(int)(pdf->pan_y*(pdf->zoom/oldz));
            snprintf(pdf->status,INFO_LEN,"PDF: %s\r\nPage %d of %d\r\nZoom: %.0f%%",
                     pdf->basename,pdf->page_index+1,pdf->page_count,pdf->zoom*100.0);
            InvalidateRect(hwnd,NULL,TRUE);
            return 0;
        }
        if(g_sel_kind==SEL_LEAN&&g_sel_idx>=0){
            LeanDoc *doc=&g_lean[g_sel_idx];
            if(doc->view_mode!=VIEW_GRAPH)return 0;
            pt.x-=SW();
            float delta=(float)GET_WHEEL_DELTA_WPARAM(wp)/WHEEL_DELTA;
            float old=doc->zoom;
            doc->zoom*=(delta>0)?1.12f:(1.0f/1.12f);
            if(doc->zoom<0.08f)doc->zoom=0.08f;
            if(doc->zoom>8.0f) doc->zoom=8.0f;
            doc->pan_x=pt.x-(int)((pt.x-doc->pan_x)*doc->zoom/old);
            doc->pan_y=pt.y-(int)((pt.y-doc->pan_y)*doc->zoom/old);
            InvalidateRect(hwnd,NULL,FALSE);
        }
        return 0;
    }

    case WM_LBUTTONDOWN: {
        int mx=GET_X_LPARAM(lp),my=GET_Y_LPARAM(lp);

        /* ---- Overlay button hit-test (main view) ---- */
        if(mx>=SW()){
            if(g_sel_kind==SEL_PDF&&g_sel_idx>=0){
                if(pt_in_rect(mx,my,g_ovl_prev)){
                    pdf_change_page(hwnd,&g_pdf[g_sel_idx],-1); return 0;}
                if(pt_in_rect(mx,my,g_ovl_next)){
                    pdf_change_page(hwnd,&g_pdf[g_sel_idx], 1); return 0;}
                if(pt_in_rect(mx,my,g_ovl_convert)){
                    convert_current_pdf(hwnd); return 0;}
            }
            if(g_sel_kind==SEL_LEAN&&g_sel_idx>=0){
                LeanDoc *doc=&g_lean[g_sel_idx];
                if(pt_in_rect(mx,my,g_ovl_graph)){
                    doc->view_mode=VIEW_GRAPH;
                    ShowWindow(g_cv_hwnd,SW_HIDE);
                    InvalidateRect(hwnd,NULL,TRUE);return 0;}
                if(pt_in_rect(mx,my,g_ovl_text)){
                    if(g_sel_node>=0) close_node_panel(hwnd);
                    doc->view_mode=VIEW_TEXT;
                    code_view_load(doc->text?doc->text:"");
                    ShowWindow(g_cv_hwnd,SW_SHOW);
                    InvalidateRect(hwnd,NULL,TRUE);return 0;}
            }
        }

        /* ---- Sidebar click ---- */
        if(mx<SW()){
            /* collapse/expand toggle */
            if(pt_in_rect(mx,my,g_sidebar_toggle_btn)){
                g_sidebar_collapsed=!g_sidebar_collapsed;
                resize_children(hwnd);
                InvalidateRect(hwnd,NULL,TRUE);
                return 0;
            }
            if(!g_sidebar_collapsed){
                SelKind kind;int idx;
                if(sidebar_hit(my,&kind,&idx)){
                    /* × close button zone (rightmost 22px of sidebar) */
                    if(mx>SW()-22){
                        if(kind==SEL_LEAN) close_lean(hwnd,idx);
                        else               close_pdf(hwnd,idx);
                        return 0;
                    }
                    if(kind==SEL_PDF){
                        /* Select PDF AND start potential drag (standalone or subrow) */
                        select_pdf(hwnd,idx);
                        g_drag_pdf_idx=idx;
                        g_drag_start_y=my;
                        g_drag_cur_y=my;
                        g_drag_cur_x=mx;
                        g_drag_active=FALSE;
                        g_drag_hover_lean=-1;
                        SetCapture(hwnd);
                    } else if(kind==SEL_LEAN){
                        select_lean(hwnd,idx);
                    }
                }
            }
            return 0;
        }

        /* ---- Main view drag (graph or PDF pan) ---- */
        if(g_sel_kind==SEL_LEAN&&g_sel_idx>=0&&g_lean[g_sel_idx].view_mode==VIEW_GRAPH){
            LeanDoc *gdoc=&g_lean[g_sel_idx];
            int hit=node_hit_test(gdoc,mx,my);
            if(hit>=0){open_node_panel(hwnd,gdoc,hit);return 0;}
            if(g_sel_node>=0) close_node_panel(hwnd);
            g_graph_dragging=TRUE;g_graph_drag_x=mx;g_graph_drag_y=my;SetCapture(hwnd);}
        else if(g_sel_kind==SEL_PDF&&g_sel_idx>=0&&g_pdf[g_sel_idx].pixels){
            PdfDoc *pdf=&g_pdf[g_sel_idx];
            pdf->dragging=TRUE;pdf->drag_x=mx;pdf->drag_y=my;SetCapture(hwnd);}
        return 0;
    }

    case WM_MOUSEMOVE: {
        int mx=GET_X_LPARAM(lp),my=GET_Y_LPARAM(lp);

        /* Overlay hover */
        if(update_hover(mx,my)) InvalidateRect(hwnd,NULL,FALSE);

        /* Sidebar drag for PDF association */
        if(g_drag_pdf_idx>=0){
            g_drag_cur_y=my;g_drag_cur_x=mx;
            if(!g_drag_active&&abs(my-g_drag_start_y)>6){
                g_drag_active=TRUE;
            }
            if(g_drag_active){
                int new_hover=sidebar_hover_lean(my);
                if(new_hover!=g_drag_hover_lean){
                    g_drag_hover_lean=new_hover;
                    InvalidateRect(hwnd,NULL,TRUE);
                } else {
                    /* repaint for ghost position */
                    RECT sr={0,0,SW(),32767};
                    InvalidateRect(hwnd,&sr,FALSE);
                }
            }
            return 0;
        }

        /* Graph pan */
        if(g_graph_dragging&&g_sel_kind==SEL_LEAN&&g_sel_idx>=0){
            LeanDoc *doc=&g_lean[g_sel_idx];
            doc->pan_x+=mx-g_graph_drag_x;doc->pan_y+=my-g_graph_drag_y;
            g_graph_drag_x=mx;g_graph_drag_y=my;
            InvalidateRect(hwnd,NULL,FALSE);}

        /* PDF pan */
        if(g_sel_kind==SEL_PDF&&g_sel_idx>=0){
            PdfDoc *pdf=&g_pdf[g_sel_idx];
            if(pdf->dragging){
                pdf->pan_x+=mx-pdf->drag_x;pdf->pan_y+=my-pdf->drag_y;
                pdf->drag_x=mx;pdf->drag_y=my;
                InvalidateRect(hwnd,NULL,FALSE);}}
        return 0;
    }

    case WM_LBUTTONUP: {
        /* Finalize drag-and-drop */
        if(g_drag_pdf_idx>=0){
            if(g_drag_active){
                if(g_drag_hover_lean>=0){
                    g_pdf[g_drag_pdf_idx].lean_idx=g_drag_hover_lean;
                    snprintf(g_pdf[g_drag_pdf_idx].status,INFO_LEN,
                             "PDF: %s\r\nPage %d of %d\r\nLinked: %s",
                             g_pdf[g_drag_pdf_idx].basename,
                             g_pdf[g_drag_pdf_idx].page_index+1,
                             g_pdf[g_drag_pdf_idx].page_count,
                             g_lean[g_drag_hover_lean].basename);
                } else {
                    g_pdf[g_drag_pdf_idx].lean_idx=-1;
                    snprintf(g_pdf[g_drag_pdf_idx].status,INFO_LEN,
                             "PDF: %s\r\nPage %d of %d",
                             g_pdf[g_drag_pdf_idx].basename,
                             g_pdf[g_drag_pdf_idx].page_index+1,
                             g_pdf[g_drag_pdf_idx].page_count);
                }
            }
            g_drag_pdf_idx=-1;g_drag_active=FALSE;g_drag_hover_lean=-1;
            ReleaseCapture();
            InvalidateRect(hwnd,NULL,TRUE);
            return 0;
        }
        g_graph_dragging=FALSE;
        if(g_sel_kind==SEL_PDF&&g_sel_idx>=0) g_pdf[g_sel_idx].dragging=FALSE;
        ReleaseCapture();
        return 0;
    }

    case WM_TIMER:
        if(wp==IDT_CONV_POLL&&g_np_conv_proc!=INVALID_HANDLE_VALUE){
            DWORD ec=STILL_ACTIVE;
            GetExitCodeProcess(g_np_conv_proc,&ec);
            if(ec!=STILL_ACTIVE){
                CloseHandle(g_np_conv_proc);g_np_conv_proc=INVALID_HANDLE_VALUE;
                KillTimer(hwnd,IDT_CONV_POLL);
                if(ec==0){
                    int pdf_ok=0;
                    if(g_pdfium.initialized||pdfium_load(NULL))
                        pdf_ok=np_tex_load_pdf();
                    if(!pdf_ok){
                        char *tex2=NULL;DWORD tlen2=0;
                        if(read_entire_file(g_np_tex_path,&tex2,&tlen2)){
                            np_tex_load(tex2);free(tex2);g_np_tex_state=2;
                        } else {g_np_tex_state=3;}
                    } else {g_np_tex_state=2;}
                } else {g_np_tex_state=3;}
                if(g_np_hwnd&&IsWindowVisible(g_np_hwnd))
                    InvalidateRect(g_np_hwnd,NULL,TRUE);
            }
        }
        return 0;

    case WM_DESTROY:
        code_view_free();
        np_free();
        np_tex_free();
        if(g_np_conv_proc!=INVALID_HANDLE_VALUE){
            TerminateProcess(g_np_conv_proc,1);CloseHandle(g_np_conv_proc);
        }
        for(int i=0;i<g_npdf;i++) pdf_close(&g_pdf[i]);
        for(int i=0;i<g_nlean;i++) free(g_lean[i].text);
        if(g_pdfium.initialized&&g_pdfium.DestroyLibrary) g_pdfium.DestroyLibrary();
        if(g_pdfium.dll) FreeLibrary(g_pdfium.dll);
        DeleteObject(g_ui_font);DeleteObject(g_mono_font);
        PostQuitMessage(0);
        return 0;
    }
    return DefWindowProcA(hwnd,msg,wp,lp);
}

/* ================================================================
   Entry point
   ================================================================ */

int WINAPI WinMain(HINSTANCE hi, HINSTANCE hpi, LPSTR cmdline, int show)
{
    (void)hpi;
    /* Register code view window class (Unicode) */
    WNDCLASSW cv_wc={0};
    cv_wc.style=CS_HREDRAW|CS_VREDRAW;
    cv_wc.lpfnWndProc=CodeViewWndProc;
    cv_wc.hInstance=hi;
    cv_wc.hbrBackground=(HBRUSH)GetStockObject(BLACK_BRUSH);
    cv_wc.lpszClassName=L"ProofVizCode";
    RegisterClassW(&cv_wc);

    WNDCLASSW np_wc={0};
    np_wc.style=CS_HREDRAW|CS_VREDRAW;
    np_wc.lpfnWndProc=NodePanelWndProc;
    np_wc.hInstance=hi;
    np_wc.hbrBackground=(HBRUSH)GetStockObject(BLACK_BRUSH);
    np_wc.lpszClassName=L"ProofVizNodePanel";
    RegisterClassW(&np_wc);

    WNDCLASSA wc={0};
    wc.style=CS_HREDRAW|CS_VREDRAW;wc.lpfnWndProc=WndProc;
    wc.hInstance=hi;wc.hCursor=LoadCursor(NULL,IDC_ARROW);
    wc.hbrBackground=(HBRUSH)GetStockObject(BLACK_BRUSH);
    wc.lpszClassName="LeanProofViz";
    RegisterClassA(&wc);

    g_hwnd=CreateWindowA("LeanProofViz","Lean Proof Visualizer",
                         WS_OVERLAPPEDWINDOW,CW_USEDEFAULT,CW_USEDEFAULT,
                         1280,800,NULL,NULL,hi,NULL);

    g_ui_font=CreateFontA(16,0,0,0,FW_NORMAL,0,0,0,DEFAULT_CHARSET,
                          OUT_DEFAULT_PRECIS,CLIP_DEFAULT_PRECIS,
                          CLEARTYPE_QUALITY,DEFAULT_PITCH,"Segoe UI");
    g_mono_font=CreateFontA(16,0,0,0,FW_NORMAL,0,0,0,DEFAULT_CHARSET,
                            OUT_DEFAULT_PRECIS,CLIP_DEFAULT_PRECIS,
                            CLEARTYPE_QUALITY,FIXED_PITCH,"Consolas");

    g_btn_open_lean=CreateWindowA("BUTTON","Open Lean file",
        WS_CHILD|WS_VISIBLE|BS_PUSHBUTTON,0,0,0,0,
        g_hwnd,(HMENU)IDC_OPEN_LEAN,hi,NULL);
    g_btn_open_pdf=CreateWindowA("BUTTON","Open PDF",
        WS_CHILD|WS_VISIBLE|BS_PUSHBUTTON,0,0,0,0,
        g_hwnd,(HMENU)IDC_OPEN_PDF,hi,NULL);
    g_cv_hwnd=CreateWindowExW(0,L"ProofVizCode",L"",
        WS_CHILD|WS_VSCROLL,
        SIDEBAR_W+1,TEXT_TOP_OFFSET,800,600,
        g_hwnd,(HMENU)IDC_TEXT_VIEW,hi,NULL);
    g_np_hwnd=CreateWindowExW(0,L"ProofVizNodePanel",L"",
        WS_CHILD|WS_VSCROLL,
        0,0,NODE_PANEL_W,600,
        g_hwnd,NULL,hi,NULL);

    SendMessageA(g_btn_open_lean,WM_SETFONT,(WPARAM)g_ui_font,TRUE);
    SendMessageA(g_btn_open_pdf, WM_SETFONT,(WPARAM)g_ui_font,TRUE);

    resize_children(g_hwnd);
    ShowWindow(g_hwnd,SW_MAXIMIZE);
    UpdateWindow(g_hwnd);

    if(cmdline&&*cmdline){
        char path[MAX_PATH];
        strncpy(path,cmdline,MAX_PATH-1);path[MAX_PATH-1]='\0';
        if(path[0]=='"'){memmove(path,path+1,strlen(path));char *e=strchr(path,'"');if(e)*e='\0';}
        if(has_ext(path,".lean")){int i=lean_open(g_hwnd,path);if(i>=0)select_lean(g_hwnd,i);}
        else if(has_ext(path,".pdf")){int i=pdf_open_doc(g_hwnd,path);if(i>=0)select_pdf(g_hwnd,i);}
    }

    MSG message;
    while(GetMessageA(&message,NULL,0,0)){
        TranslateMessage(&message);
        DispatchMessageA(&message);
    }
    return (int)message.wParam;
}
