/* proof_viz.c — Lean Proof Visualizer
 *
 * Parses a .lean file and renders its declarations as a layered
 * directed graph: core Lean axioms sit at the bottom; every theorem,
 * lemma, and def floats above the things it depends on.
 *
 * Build (MinGW / Git-Bash):
 *   gcc -O2 -mwindows -o proof_viz.exe main.c -lcomdlg32 -lgdi32 -luser32 -lm
 *
 * Controls:
 *   O          — open a .lean file
 *   T          — show the loaded .lean file as text
 *   G          — show the proof graph
 *   P          — import/open a PDF in the system PDF viewer
 *   drag       — pan the proof graph
 *   scroll     — zoom the proof graph
 *   Esc        — quit
 */

#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <windowsx.h>   /* GET_X_LPARAM, GET_Y_LPARAM          */
#include <commdlg.h>    /* GetOpenFileName                     */
#include <shellapi.h>   /* ShellExecute                         */
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>

/* ================================================================
   Constants
   ================================================================ */

#define MAX_NODES  512
#define MAX_EDGES 2048
#define NAME_LEN   128

#define NODE_W   150   /* node width  (world pixels) */
#define NODE_H    40   /* node height (world pixels) */
#define LAYER_H  110   /* vertical gap between layers */
#define SLOT_W   170   /* horizontal gap between nodes in a layer */

#define SIDEBAR_W 230
#define BTN_H      32
#define BTN_W     190
#define BTN_X      18
#define INFO_LEN  1024

#define IDC_OPEN_LEAN  1001
#define IDC_VIEW_GRAPH 1002
#define IDC_VIEW_TEXT  1003
#define IDC_OPEN_PDF   1004
#define IDC_TEXT_VIEW  1005

/* ================================================================
   Node kinds and their colours
   ================================================================ */

typedef enum {
    NK_AXIOM = 0,
    NK_IMPORT,
    NK_DEF,
    NK_THEOREM,
    NK_LEMMA,
    NK_COUNT
} NodeKind;

static const COLORREF KIND_COL[NK_COUNT] = {
    RGB(180,  55,  55),   /* axiom   — dark red    */
    RGB( 55, 100, 180),   /* import  — steel blue  */
    RGB( 55, 150,  75),   /* def     — forest green*/
    RGB( 90,  75, 195),   /* theorem — indigo      */
    RGB( 55, 165, 165),   /* lemma   — teal        */
};
static const char *KIND_STR[NK_COUNT] = {
    "axiom","import","def","theorem","lemma"
};

/* Orange override for any node that uses sorry */
#define SORRY_COL  RGB(210,140,40)

/* ================================================================
   Data model
   ================================================================ */

typedef struct {
    char      name[NAME_LEN];
    NodeKind  kind;
    int       has_sorry;
    int       layer;    /* 0 = axioms (bottom of screen) */
    int       slot;     /* index within layer            */
    int       wx, wy;   /* top-left in world coordinates */
} Node;

typedef struct {
    int u, v;   /* u depends on v  (u is above v in the layout) */
} Edge;

static Node  nd[MAX_NODES];
static int   nnd = 0;
static Edge  ed[MAX_EDGES];
static int   ned = 0;

typedef enum {
    VIEW_GRAPH = 0,
    VIEW_TEXT,
    VIEW_PDF
} ViewMode;

static ViewMode g_view_mode = VIEW_GRAPH;
static char g_loaded_lean[MAX_PATH] = "";
static char g_loaded_pdf[MAX_PATH]  = "";
static char g_status[INFO_LEN]      = "No file loaded.";

/* ================================================================
   Graph helpers
   ================================================================ */

static int node_find(const char *s)
{
    for (int i = 0; i < nnd; i++)
        if (strcmp(nd[i].name, s) == 0) return i;
    return -1;
}

static int node_add(const char *s, NodeKind k)
{
    int i = node_find(s);
    if (i >= 0) {
        /* prefer the more "fundamental" kind if we see the same name twice */
        if ((int)k < (int)nd[i].kind) nd[i].kind = k;
        return i;
    }
    if (nnd >= MAX_NODES) return -1;
    i = nnd++;
    strncpy(nd[i].name, s, NAME_LEN - 1);
    nd[i].kind      = k;
    nd[i].has_sorry = 0;
    nd[i].layer     = -1;
    nd[i].slot      = 0;
    nd[i].wx        = 0;
    nd[i].wy        = 0;
    return i;
}

static void edge_add(int u, int v)
{
    if (u < 0 || v < 0 || u == v) return;
    for (int i = 0; i < ned; i++)
        if (ed[i].u == u && ed[i].v == v) return;
    if (ned >= MAX_EDGES) return;
    ed[ned].u = u;
    ed[ned].v = v;
    ned++;
}

/* ================================================================
   Parser
   ================================================================ */

#define N_CORE_AXIOMS 4
static const char *CORE_AXIOMS[N_CORE_AXIOMS] = {
    "propext", "Classical.choice", "Quot.sound", "funext"
};

static void rtrim(char *s)
{
    int n = (int)strlen(s) - 1;
    while (n >= 0 && (s[n]=='\r'||s[n]=='\n'||s[n]==' '||s[n]=='\t'))
        s[n--] = '\0';
}

static void ltrim(char *s)
{
    int i = 0;
    while (s[i]==' '||s[i]=='\t') i++;
    if (i) memmove(s, s+i, strlen(s+i)+1);
}

/* Copy the first Lean identifier token from src into dst[dsz].
   Returns pointer to first character after the token. */
static const char *lex_ident(const char *src, char *dst, int dsz)
{
    while (*src==' '||*src=='\t') src++;
    int i = 0;
    while (*src && *src!=' ' && *src!='\t' && *src!='(' &&
           *src!=')' && *src!=':' && *src!='[' && *src!='{' &&
           *src!=',' && i < dsz-1)
        dst[i++] = *src++;
    dst[i] = '\0';
    return src;
}

static int is_id_char(char c)
{
    return (c>='a'&&c<='z')||(c>='A'&&c<='Z')||
           (c>='0'&&c<='9')|| c=='_' || c=='.';
}

/* Return 1 if needle appears as a whole "word" in haystack. */
static int word_in(const char *hay, const char *needle)
{
    int nlen = (int)strlen(needle);
    if (!nlen) return 0;
    const char *p = hay;
    while ((p = strstr(p, needle)) != NULL) {
        char before = (p > hay) ? p[-1] : '\0';
        char after  = p[nlen];
        if (!is_id_char(before) && !is_id_char(after)) return 1;
        p += nlen;
    }
    return 0;
}

/* Skip @[attrib] attribute annotations and leading modifier keywords. */
static const char *skip_modifiers(const char *p)
{
    again:
    while (*p==' '||*p=='\t') p++;
    if (*p == '@') {
        const char *cl = strchr(p, ']');
        if (cl) { p = cl+1; goto again; }
    }
    static const char *mods[] = {
        "noncomputable ","private ","protected ",
        "partial ","unsafe ","scoped ","irreducible "
    };
    for (int m = 0; m < 7; m++) {
        size_t ml = strlen(mods[m]);
        if (strncmp(p, mods[m], ml) == 0) { p += ml; goto again; }
    }
    return p;
}

/* Identify a declaration keyword at position p.
   Sets *kind and returns the length of the keyword (incl. trailing space),
   or 0 if not a declaration. */
static int decl_keyword(const char *p, NodeKind *kind)
{
    struct { const char *kw; NodeKind k; } kws[] = {
        {"theorem ",  NK_THEOREM},
        {"lemma ",    NK_LEMMA},
        {"def ",      NK_DEF},
        {"abbrev ",   NK_DEF},
        {"axiom ",    NK_AXIOM},
        {"opaque ",   NK_DEF},
    };
    for (int i = 0; i < 6; i++) {
        size_t l = strlen(kws[i].kw);
        if (strncmp(p, kws[i].kw, l) == 0) { *kind = kws[i].k; return (int)l; }
    }
    return 0;
}

static void parse_file(const char *path)
{
    nnd = 0;
    ned = 0;

    /* Core Lean 4 axioms are always present */
    for (int i = 0; i < N_CORE_AXIOMS; i++)
        node_add(CORE_AXIOMS[i], NK_AXIOM);

    FILE *f = fopen(path, "r");
    if (!f) return;

    char line[4096];

    /* ---- Pass 1: collect all declaration names ---- */
    while (fgets(line, sizeof(line), f)) {
        rtrim(line); ltrim(line);
        if (line[0]=='-' && line[1]=='-') continue;   /* line comment */
        if (line[0]=='/' && line[1]=='*') continue;   /* block comment start */

        /* import */
        if (strncmp(line, "import ", 7) == 0) {
            char nm[NAME_LEN];
            lex_ident(line+7, nm, NAME_LEN);
            if (nm[0]) node_add(nm, NK_IMPORT);
            continue;
        }

        const char *p = skip_modifiers(line);
        NodeKind k;
        int kl = decl_keyword(p, &k);
        if (!kl) continue;

        char nm[NAME_LEN];
        lex_ident(p + kl, nm, NAME_LEN);
        if (nm[0]) node_add(nm, k);
    }

    /* ---- Pass 2: find dependencies by scanning bodies ---- */
    rewind(f);
    int cur = -1;

    while (fgets(line, sizeof(line), f)) {
        rtrim(line); ltrim(line);
        if (line[0]=='-' && line[1]=='-') continue;

        /* Detect the start of a new declaration */
        const char *p = skip_modifiers(line);
        int kl = 0;
        NodeKind k;

        if (strncmp(line, "import ", 7) == 0) {
            char nm[NAME_LEN]; lex_ident(line+7, nm, NAME_LEN);
            cur = node_find(nm);
            kl  = 1; /* mark as handled */
        } else {
            kl = decl_keyword(p, &k);
            if (kl) {
                char nm[NAME_LEN]; lex_ident(p+kl, nm, NAME_LEN);
                cur = node_find(nm);
            }
        }

        if (cur < 0) continue;

        /* sorry detection */
        if (strstr(line, "sorry")) nd[cur].has_sorry = 1;

        /* Reference scan: does any known name appear on this line? */
        for (int i = 0; i < nnd; i++) {
            if (i == cur) continue;
            if (word_in(line, nd[i].name))
                edge_add(cur, i);
        }
    }

    fclose(f);

    /* Every import implicitly depends on the four core axioms */
    for (int i = 0; i < nnd; i++)
        if (nd[i].kind == NK_IMPORT)
            for (int j = 0; j < N_CORE_AXIOMS; j++)
                edge_add(i, node_find(CORE_AXIOMS[j]));
}

/* ================================================================
   Layout  (longest-path layering + even horizontal spacing)
   ================================================================ */

static int layer_sz[MAX_NODES]; /* nodes per layer */

static void layout(void)
{
    /* Reset layers */
    for (int i = 0; i < nnd; i++) nd[i].layer = -1;

    /* Axioms sit at layer 0 */
    for (int i = 0; i < nnd; i++)
        if (nd[i].kind == NK_AXIOM) nd[i].layer = 0;

    /* Propagate: nd[u].layer = max(nd[v].layer)+1 for all edges u→v */
    int changed = 1;
    while (changed) {
        changed = 0;
        for (int e = 0; e < ned; e++) {
            int u = ed[e].u, v = ed[e].v;
            if (nd[v].layer < 0) continue;
            int want = nd[v].layer + 1;
            if (nd[u].layer < want) { nd[u].layer = want; changed = 1; }
        }
    }

    /* Anything still unassigned floats just above axioms */
    for (int i = 0; i < nnd; i++)
        if (nd[i].layer < 0) nd[i].layer = 1;

    /* Find max layer */
    int max_layer = 0;
    for (int i = 0; i < nnd; i++)
        if (nd[i].layer > max_layer) max_layer = nd[i].layer;

    /* Count nodes per layer and assign horizontal slots */
    memset(layer_sz, 0, sizeof(int) * (max_layer + 2));
    for (int i = 0; i < nnd; i++)
        nd[i].slot = layer_sz[nd[i].layer]++;

    /* World-space positions:
       y: layer 0 at BOTTOM  →  wy = (max_layer − layer) × LAYER_H
       x: centred within the widest layer                              */
    int max_in_layer = 0;
    for (int i = 0; i <= max_layer; i++)
        if (layer_sz[i] > max_in_layer) max_in_layer = layer_sz[i];

    for (int i = 0; i < nnd; i++) {
        int lsz    = layer_sz[nd[i].layer];
        int offset = (max_in_layer * SLOT_W - lsz * SLOT_W) / 2;
        nd[i].wx   = offset + nd[i].slot * SLOT_W;
        nd[i].wy   = (max_layer - nd[i].layer) * LAYER_H;
    }
}

/* ================================================================
   Renderer
   ================================================================ */

static float g_zoom   = 1.0f;
static int   g_pan_x  = 60;
static int   g_pan_y  = 40;
static int   g_drag_x, g_drag_y;
static BOOL  g_dragging = FALSE;

static void w2s(int wx, int wy, int *sx, int *sy)
{
    *sx = SIDEBAR_W + (int)(wx * g_zoom) + g_pan_x;
    *sy = (int)(wy * g_zoom) + g_pan_y;
}

static void draw_arrow(HDC dc, int x1, int y1, int x2, int y2, COLORREF col)
{
    HPEN pen = CreatePen(PS_SOLID, 1, col);
    HPEN old = SelectObject(dc, pen);

    MoveToEx(dc, x1, y1, NULL);
    LineTo  (dc, x2, y2);

    /* arrowhead */
    double dx = x2 - x1, dy = y2 - y1;
    double len = sqrt(dx*dx + dy*dy);
    if (len > 1.0) {
        dx /= len; dy /= len;
        int al = 9;
        int ax1 = x2 - (int)(al*(dx + dy*0.5));
        int ay1 = y2 - (int)(al*(dy - dx*0.5));
        int ax2 = x2 - (int)(al*(dx - dy*0.5));
        int ay2 = y2 - (int)(al*(dy + dx*0.5));
        MoveToEx(dc, x2, y2, NULL); LineTo(dc, ax1, ay1);
        MoveToEx(dc, x2, y2, NULL); LineTo(dc, ax2, ay2);
    }

    SelectObject(dc, old);
    DeleteObject(pen);
}

static void draw_node(HDC dc, int i)
{
    int sx, sy;
    w2s(nd[i].wx, nd[i].wy, &sx, &sy);
    int w = (int)(NODE_W * g_zoom);
    int h = (int)(NODE_H * g_zoom);

    COLORREF bg = nd[i].has_sorry ? SORRY_COL : KIND_COL[nd[i].kind];

    /* filled rounded rect */
    HBRUSH br  = CreateSolidBrush(bg);
    HPEN   pn  = CreatePen(PS_SOLID, 1, RGB(220,220,220));
    HBRUSH obr = SelectObject(dc, br);
    HPEN   opn = SelectObject(dc, pn);
    RoundRect(dc, sx, sy, sx+w, sy+h, 10, 10);
    SelectObject(dc, obr);
    SelectObject(dc, opn);
    DeleteObject(br);
    DeleteObject(pn);

    /* name label */
    SetTextColor(dc, RGB(255,255,255));
    SetBkMode   (dc, TRANSPARENT);
    RECT tr = { sx+4, sy, sx+w-4, sy+h };
    DrawTextA(dc, nd[i].name, -1, &tr,
              DT_CENTER | DT_VCENTER | DT_SINGLELINE | DT_END_ELLIPSIS);
}

static void draw_graph(HDC dc)
{
    /* Edges first (drawn behind nodes) */
    for (int e = 0; e < ned; e++) {
        int u = ed[e].u, v = ed[e].v;
        /* arrow tail: top-centre of v (lower layer)
           arrow head: bottom-centre of u (higher layer)       */
        int tx, ty, hx, hy;
        w2s(nd[v].wx + NODE_W/2, nd[v].wy,         &tx, &ty);   /* v top    */
        w2s(nd[u].wx + NODE_W/2, nd[u].wy + NODE_H, &hx, &hy);  /* u bottom */
        draw_arrow(dc, tx, ty, hx, hy, RGB(120,120,140));
    }

    /* Nodes */
    for (int i = 0; i < nnd; i++)
        draw_node(dc, i);
}

static void draw_legend(HDC dc)
{
    struct { const char *label; COLORREF col; } entries[] = {
        {"axiom",        KIND_COL[NK_AXIOM]},
        {"import",       KIND_COL[NK_IMPORT]},
        {"def / abbrev", KIND_COL[NK_DEF]},
        {"theorem",      KIND_COL[NK_THEOREM]},
        {"lemma",        KIND_COL[NK_LEMMA]},
        {"uses sorry",   SORRY_COL},
    };
    int n = sizeof(entries) / sizeof(entries[0]);

    for (int i = 0; i < n; i++) {
        int x = 10, y = 10 + i * 20;
        HBRUSH b = CreateSolidBrush(entries[i].col);
        HPEN   p = CreatePen(PS_SOLID, 1, RGB(200,200,200));
        SelectObject(dc, b); SelectObject(dc, p);
        RoundRect(dc, x, y, x+14, y+13, 3, 3);
        DeleteObject(b); DeleteObject(p);
        SetTextColor(dc, RGB(180,180,200));
        SetBkMode   (dc, TRANSPARENT);
        TextOutA(dc, x+18, y, entries[i].label, (int)strlen(entries[i].label));
    }
}

/* ================================================================
   Win32 window
   ================================================================ */

static HWND g_hwnd;
static HWND g_text_hwnd;
static HWND g_btn_open_lean;
static HWND g_btn_view_graph;
static HWND g_btn_view_text;
static HWND g_btn_open_pdf;
static HFONT g_ui_font;
static HFONT g_mono_font;

static void set_status(const char *fmt, ...)
{
    va_list ap;
    va_start(ap, fmt);
    vsnprintf(g_status, sizeof(g_status), fmt, ap);
    va_end(ap);
    g_status[sizeof(g_status)-1] = '\0';
}

static int has_ext(const char *path, const char *ext)
{
    size_t lp = strlen(path), le = strlen(ext);
    if (lp < le) return 0;
    return lstrcmpiA(path + lp - le, ext) == 0;
}

static int read_entire_file(const char *path, char **out, DWORD *out_len)
{
    HANDLE h = CreateFileA(path, GENERIC_READ, FILE_SHARE_READ, NULL,
                           OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
    if (h == INVALID_HANDLE_VALUE) return 0;

    LARGE_INTEGER size;
    if (!GetFileSizeEx(h, &size) || size.QuadPart > 50 * 1024 * 1024) {
        CloseHandle(h);
        return 0;
    }

    DWORD len = (DWORD)size.QuadPart;
    char *buf = (char *)malloc(len + 1);
    if (!buf) {
        CloseHandle(h);
        return 0;
    }

    DWORD got = 0;
    BOOL ok = ReadFile(h, buf, len, &got, NULL);
    CloseHandle(h);

    if (!ok) {
        free(buf);
        return 0;
    }

    buf[got] = '\0';
    *out = buf;
    if (out_len) *out_len = got;
    return 1;
}

static void resize_children(HWND hwnd)
{
    RECT cr;
    GetClientRect(hwnd, &cr);
    int right_x = SIDEBAR_W + 1;
    int right_w = cr.right - right_x;
    if (right_w < 1) right_w = 1;

    MoveWindow(g_btn_open_lean,  BTN_X,  58, BTN_W, BTN_H, TRUE);
    MoveWindow(g_btn_view_graph, BTN_X, 100, BTN_W, BTN_H, TRUE);
    MoveWindow(g_btn_view_text,  BTN_X, 142, BTN_W, BTN_H, TRUE);
    MoveWindow(g_btn_open_pdf,   BTN_X, 184, BTN_W, BTN_H, TRUE);

    MoveWindow(g_text_hwnd, right_x, 0, right_w, cr.bottom, TRUE);
}

static void update_visible_view(HWND hwnd)
{
    ShowWindow(g_text_hwnd, g_view_mode == VIEW_TEXT ? SW_SHOW : SW_HIDE);
    InvalidateRect(hwnd, NULL, TRUE);
}

static void load_lean_file(HWND hwnd, const char *path)
{
    parse_file(path);
    layout();

    strncpy(g_loaded_lean, path, MAX_PATH - 1);
    g_loaded_lean[MAX_PATH - 1] = '\0';

    char *contents = NULL;
    DWORD len = 0;
    if (read_entire_file(path, &contents, &len)) {
        SetWindowTextA(g_text_hwnd, contents);
        free(contents);
    } else {
        SetWindowTextA(g_text_hwnd, "Could not load Lean source text.");
    }

    g_zoom  = 1.0f;
    g_pan_x = 60;
    g_pan_y = 40;
    g_view_mode = VIEW_GRAPH;
    set_status("Loaded Lean file:\r\n%s\r\n\r\nNodes: %d\r\nEdges: %d", path, nnd, ned);
    update_visible_view(hwnd);
}

static void open_lean_file(HWND hwnd)
{
    OPENFILENAMEA ofn = {0};
    char fn[MAX_PATH]  = {0};
    ofn.lStructSize = sizeof(ofn);
    ofn.hwndOwner   = hwnd;
    ofn.lpstrFilter = "Lean Files\0*.lean\0All Files\0*.*\0";
    ofn.lpstrFile   = fn;
    ofn.nMaxFile    = MAX_PATH;
    ofn.Flags       = OFN_FILEMUSTEXIST | OFN_PATHMUSTEXIST;
    if (GetOpenFileNameA(&ofn)) {
        if (!has_ext(fn, ".lean")) {
            MessageBoxA(hwnd, "Please choose a .lean file.", "Unsupported file", MB_ICONWARNING);
            return;
        }
        load_lean_file(hwnd, fn);
    }
}

static void open_pdf_file(HWND hwnd)
{
    OPENFILENAMEA ofn = {0};
    char fn[MAX_PATH]  = {0};
    ofn.lStructSize = sizeof(ofn);
    ofn.hwndOwner   = hwnd;
    ofn.lpstrFilter = "PDF Files\0*.pdf\0All Files\0*.*\0";
    ofn.lpstrFile   = fn;
    ofn.nMaxFile    = MAX_PATH;
    ofn.Flags       = OFN_FILEMUSTEXIST | OFN_PATHMUSTEXIST;
    if (GetOpenFileNameA(&ofn)) {
        if (!has_ext(fn, ".pdf")) {
            MessageBoxA(hwnd, "Please choose a .pdf file.", "Unsupported file", MB_ICONWARNING);
            return;
        }

        strncpy(g_loaded_pdf, fn, MAX_PATH - 1);
        g_loaded_pdf[MAX_PATH - 1] = '\0';
        g_view_mode = VIEW_PDF;
        set_status("Imported PDF:\r\n%s\r\n\r\nThe PDF is opened with your default PDF viewer.\r\nFor true in-window PDF rendering, add PDFium, MuPDF, Poppler, or WebView2.", fn);
        update_visible_view(hwnd);

        ShellExecuteA(hwnd, "open", fn, NULL, NULL, SW_SHOWNORMAL);
    }
}

static LRESULT CALLBACK WndProc(HWND hwnd, UINT msg, WPARAM wp, LPARAM lp)
{
    switch (msg) {

    case WM_PAINT: {
        PAINTSTRUCT ps;
        HDC hdc = BeginPaint(hwnd, &ps);
        RECT cr; GetClientRect(hwnd, &cr);

        /* double-buffer to avoid flicker */
        HDC     mdc = CreateCompatibleDC(hdc);
        HBITMAP bmp = CreateCompatibleBitmap(hdc, cr.right, cr.bottom);
        SelectObject(mdc, bmp);

        /* background */
        HBRUSH bg = CreateSolidBrush(RGB(22, 22, 32));
        FillRect(mdc, &cr, bg);
        DeleteObject(bg);

        HFONT font = CreateFontA(
            12, 0, 0, 0, FW_NORMAL, 0, 0, 0, DEFAULT_CHARSET,
            OUT_DEFAULT_PRECIS, CLIP_DEFAULT_PRECIS,
            CLEARTYPE_QUALITY, DEFAULT_PITCH, "Segoe UI");
        HFONT old_font = SelectObject(mdc, font);

        /* sidebar */
        RECT sr = {0, 0, SIDEBAR_W, cr.bottom};
        HBRUSH sb = CreateSolidBrush(RGB(30, 30, 42));
        FillRect(mdc, &sr, sb);
        DeleteObject(sb);
        HPEN sep = CreatePen(PS_SOLID, 1, RGB(55,55,70));
        HPEN old_sep = SelectObject(mdc, sep);
        MoveToEx(mdc, SIDEBAR_W, 0, NULL);
        LineTo(mdc, SIDEBAR_W, cr.bottom);
        SelectObject(mdc, old_sep);
        DeleteObject(sep);

        SetTextColor(mdc, RGB(235,235,245));
        SetBkMode(mdc, TRANSPARENT);
        RECT title = {BTN_X, 18, SIDEBAR_W - 12, 44};
        DrawTextA(mdc, "ProofViz", -1, &title, DT_LEFT | DT_VCENTER | DT_SINGLELINE);

        SetTextColor(mdc, RGB(180,180,200));
        RECT ir = {BTN_X, 235, SIDEBAR_W - 14, cr.bottom - 12};
        DrawTextA(mdc, g_status, -1, &ir, DT_LEFT | DT_WORDBREAK);

        RECT vr = {SIDEBAR_W + 1, 0, cr.right, cr.bottom};

        if (g_view_mode == VIEW_GRAPH) {
            HRGN clip = CreateRectRgn(vr.left, vr.top, vr.right, vr.bottom);
            SelectClipRgn(mdc, clip);

            if (nnd > 0) {
                draw_graph(mdc);
            } else {
                SetTextColor(mdc, RGB(100,100,120));
                SetBkMode(mdc, TRANSPARENT);
                DrawTextA(mdc, "Open a .lean file to view its proof tree", -1, &vr,
                          DT_CENTER | DT_VCENTER | DT_SINGLELINE);
            }

            draw_legend(mdc);
            SelectClipRgn(mdc, NULL);
            DeleteObject(clip);

            SetTextColor(mdc, RGB(70,70,90));
            SetBkMode(mdc, TRANSPARENT);
            RECT hr = {cr.right-290, cr.bottom-18, cr.right-4, cr.bottom};
            DrawTextA(mdc, "O=open Lean   T=text   G=graph   P=PDF", -1, &hr, DT_LEFT);
        } else if (g_view_mode == VIEW_PDF) {
            SetTextColor(mdc, RGB(170,170,190));
            SetBkMode(mdc, TRANSPARENT);
            const char *msg = g_loaded_pdf[0]
                ? "PDF imported. It has been opened in your default PDF viewer."
                : "Open a PDF from the sidebar.";
            DrawTextA(mdc, msg, -1, &vr, DT_CENTER | DT_VCENTER | DT_SINGLELINE);
        }

        SelectObject(mdc, old_font);
        DeleteObject(font);

        BitBlt(hdc, 0, 0, cr.right, cr.bottom, mdc, 0, 0, SRCCOPY);
        DeleteObject(bmp);
        DeleteDC(mdc);

        EndPaint(hwnd, &ps);
        return 0;
    }

    case WM_COMMAND:
        switch (LOWORD(wp)) {
        case IDC_OPEN_LEAN:
            open_lean_file(hwnd);
            return 0;
        case IDC_VIEW_GRAPH:
            g_view_mode = VIEW_GRAPH;
            update_visible_view(hwnd);
            return 0;
        case IDC_VIEW_TEXT:
            if (g_loaded_lean[0]) {
                g_view_mode = VIEW_TEXT;
                update_visible_view(hwnd);
            } else {
                MessageBoxA(hwnd, "Open a .lean file first.", "No Lean file", MB_ICONINFORMATION);
            }
            return 0;
        case IDC_OPEN_PDF:
            open_pdf_file(hwnd);
            return 0;
        }
        break;

    case WM_SIZE:
        resize_children(hwnd);
        return 0;

    case WM_KEYDOWN:
        if (wp == 'O')        open_lean_file(hwnd);
        if (wp == 'T' && g_loaded_lean[0]) { g_view_mode = VIEW_TEXT; update_visible_view(hwnd); }
        if (wp == 'G')        { g_view_mode = VIEW_GRAPH; update_visible_view(hwnd); }
        if (wp == 'P')        open_pdf_file(hwnd);
        if (wp == VK_ESCAPE)  PostQuitMessage(0);
        return 0;

    case WM_MOUSEWHEEL: {
        /* zoom toward the cursor */
        if (g_view_mode != VIEW_GRAPH) return 0;
        POINT pt = { GET_X_LPARAM(lp), GET_Y_LPARAM(lp) };
        ScreenToClient(hwnd, &pt);
        if (pt.x < SIDEBAR_W) return 0;
        pt.x -= SIDEBAR_W;
        float delta = (float)GET_WHEEL_DELTA_WPARAM(wp) / WHEEL_DELTA;
        float old   = g_zoom;
        g_zoom *= (delta > 0) ? 1.12f : (1.0f/1.12f);
        if (g_zoom < 0.08f) g_zoom = 0.08f;
        if (g_zoom > 8.0f)  g_zoom = 8.0f;
        g_pan_x = pt.x - (int)((pt.x - g_pan_x) * g_zoom / old);
        g_pan_y = pt.y - (int)((pt.y - g_pan_y) * g_zoom / old);
        InvalidateRect(hwnd, NULL, FALSE);
        return 0;
    }

    case WM_LBUTTONDOWN:
        if (g_view_mode == VIEW_GRAPH && GET_X_LPARAM(lp) >= SIDEBAR_W) {
            g_dragging = TRUE;
            g_drag_x   = GET_X_LPARAM(lp);
            g_drag_y   = GET_Y_LPARAM(lp);
            SetCapture(hwnd);
        }
        return 0;

    case WM_MOUSEMOVE:
        if (g_dragging) {
            int mx = GET_X_LPARAM(lp), my = GET_Y_LPARAM(lp);
            g_pan_x += mx - g_drag_x;
            g_pan_y += my - g_drag_y;
            g_drag_x = mx;
            g_drag_y = my;
            InvalidateRect(hwnd, NULL, FALSE);
        }
        return 0;

    case WM_LBUTTONUP:
        g_dragging = FALSE;
        ReleaseCapture();
        return 0;

    case WM_DESTROY:
        if (g_ui_font) DeleteObject(g_ui_font);
        if (g_mono_font) DeleteObject(g_mono_font);
        PostQuitMessage(0);
        return 0;
    }
    return DefWindowProcA(hwnd, msg, wp, lp);
}

/* ================================================================
   Entry point
   ================================================================ */

int WINAPI WinMain(HINSTANCE hi, HINSTANCE hpi, LPSTR cmdline, int show)
{
    (void)hpi;

    WNDCLASSA wc    = {0};
    wc.style        = CS_HREDRAW | CS_VREDRAW;
    wc.lpfnWndProc  = WndProc;
    wc.hInstance    = hi;
    wc.hCursor      = LoadCursor(NULL, IDC_ARROW);
    wc.hbrBackground= (HBRUSH)GetStockObject(BLACK_BRUSH);
    wc.lpszClassName= "LeanProofViz";
    RegisterClassA(&wc);

    g_hwnd = CreateWindowA(
        "LeanProofViz", "Lean Proof Visualizer",
        WS_OVERLAPPEDWINDOW | WS_VISIBLE,
        CW_USEDEFAULT, CW_USEDEFAULT, 1280, 800,
        NULL, NULL, hi, NULL);

    g_ui_font = CreateFontA(
        16, 0, 0, 0, FW_NORMAL, 0, 0, 0, DEFAULT_CHARSET,
        OUT_DEFAULT_PRECIS, CLIP_DEFAULT_PRECIS,
        CLEARTYPE_QUALITY, DEFAULT_PITCH, "Segoe UI");
    g_mono_font = CreateFontA(
        16, 0, 0, 0, FW_NORMAL, 0, 0, 0, DEFAULT_CHARSET,
        OUT_DEFAULT_PRECIS, CLIP_DEFAULT_PRECIS,
        CLEARTYPE_QUALITY, FIXED_PITCH, "Consolas");

    g_btn_open_lean = CreateWindowA("BUTTON", "Open Lean file",
        WS_CHILD | WS_VISIBLE | BS_PUSHBUTTON,
        0, 0, 0, 0, g_hwnd, (HMENU)IDC_OPEN_LEAN, hi, NULL);
    g_btn_view_graph = CreateWindowA("BUTTON", "Proof tree view",
        WS_CHILD | WS_VISIBLE | BS_PUSHBUTTON,
        0, 0, 0, 0, g_hwnd, (HMENU)IDC_VIEW_GRAPH, hi, NULL);
    g_btn_view_text = CreateWindowA("BUTTON", "Lean text view",
        WS_CHILD | WS_VISIBLE | BS_PUSHBUTTON,
        0, 0, 0, 0, g_hwnd, (HMENU)IDC_VIEW_TEXT, hi, NULL);
    g_btn_open_pdf = CreateWindowA("BUTTON", "Open PDF",
        WS_CHILD | WS_VISIBLE | BS_PUSHBUTTON,
        0, 0, 0, 0, g_hwnd, (HMENU)IDC_OPEN_PDF, hi, NULL);

    g_text_hwnd = CreateWindowExA(WS_EX_CLIENTEDGE, "EDIT", "",
        WS_CHILD | WS_VSCROLL | WS_HSCROLL | ES_MULTILINE | ES_READONLY |
        ES_AUTOHSCROLL | ES_AUTOVSCROLL,
        SIDEBAR_W + 1, 0, 800, 600,
        g_hwnd, (HMENU)IDC_TEXT_VIEW, hi, NULL);

    SendMessageA(g_btn_open_lean,  WM_SETFONT, (WPARAM)g_ui_font, TRUE);
    SendMessageA(g_btn_view_graph, WM_SETFONT, (WPARAM)g_ui_font, TRUE);
    SendMessageA(g_btn_view_text,  WM_SETFONT, (WPARAM)g_ui_font, TRUE);
    SendMessageA(g_btn_open_pdf,   WM_SETFONT, (WPARAM)g_ui_font, TRUE);
    SendMessageA(g_text_hwnd,      WM_SETFONT, (WPARAM)g_mono_font, TRUE);

    resize_children(g_hwnd);
    update_visible_view(g_hwnd);

    /* Optional: load file passed on the command line */
    if (cmdline && *cmdline) {
        char path[MAX_PATH];
        strncpy(path, cmdline, MAX_PATH - 1);
        path[MAX_PATH - 1] = '\0';
        /* strip surrounding quotes if present */
        if (path[0] == '"') {
            memmove(path, path + 1, strlen(path));
            char *end = strchr(path, '"');
            if (end) *end = '\0';
        }
        if (has_ext(path, ".lean")) {
            load_lean_file(g_hwnd, path);
        } else if (has_ext(path, ".pdf")) {
            strncpy(g_loaded_pdf, path, MAX_PATH - 1);
            g_loaded_pdf[MAX_PATH - 1] = '\0';
            g_view_mode = VIEW_PDF;
            set_status("Imported PDF:\r\n%s", path);
            update_visible_view(g_hwnd);
            ShellExecuteA(g_hwnd, "open", path, NULL, NULL, SW_SHOWNORMAL);
        }
    }

    MSG msg;
    while (GetMessageA(&msg, NULL, 0, 0)) {
        TranslateMessage(&msg);
        DispatchMessageA(&msg);
    }
    return (int)msg.wParam;
}
