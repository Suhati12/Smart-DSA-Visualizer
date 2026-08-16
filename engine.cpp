##
#include <iostream>
#include <stack>
#include <string>
#include <vector>
#include <queue>
#include <unordered_map>
#include <unordered_set>
#include <set>
#include <algorithm>
using namespace std;

// ═══════════════════════════════════════════════════════
//  1. INFIX → POSTFIX / PREFIX
// ═══════════════════════════════════════════════════════
int precedence(char op) {
    if (op == '+' || op == '-') return 1;
    if (op == '*' || op == '/') return 2;
    if (op == '^')              return 3;
    return 0;
}
bool isOp(char c) { return string("+-*/^").find(c) != string::npos; }

void infixToPostfix(const string& expr) {
    stack<char> st;
    string out;
    cout << "POSTFIX_STEPS\n";
    for (char c : expr) {
        if (c == ' ') continue;
        if (isalnum(c)) {
            out += c;
            cout << "STEP OPERAND " << c << " " << out << "\n";
        } else if (c == '(') {
            st.push(c);
            cout << "STEP PUSH_PAREN ( " << out << "\n";
        } else if (c == ')') {
            while (!st.empty() && st.top() != '(') { out += st.top(); st.pop(); }
            if (!st.empty()) st.pop();
            cout << "STEP POP_PAREN ) " << out << "\n";
        } else if (isOp(c)) {
            while (!st.empty() && precedence(st.top()) >= precedence(c))
                { out += st.top(); st.pop(); }
            st.push(c);
            cout << "STEP OPERATOR " << c << " " << out << "\n";
        }
    }
    while (!st.empty()) { out += st.top(); st.pop(); }
    cout << "POSTFIX_RESULT " << out << "\n";
    cout << "POSTFIX_STEPS_END\n";
}

void infixToPrefix(const string& expr) {
    string rev = expr;
    reverse(rev.begin(), rev.end());
    for (char& c : rev) {
        if (c == '(') c = ')';
        else if (c == ')') c = '(';
    }
    stack<char> st; string out;
    for (char c : rev) {
        if (c == ' ') continue;
        if (isalnum(c)) out += c;
        else if (c == '(') st.push(c);
        else if (c == ')') {
            while (!st.empty() && st.top() != '(') { out += st.top(); st.pop(); }
            if (!st.empty()) st.pop();
        } else if (isOp(c)) {
            while (!st.empty() && precedence(st.top()) > precedence(c))
                { out += st.top(); st.pop(); }
            st.push(c);
        }
    }
    while (!st.empty()) { out += st.top(); st.pop(); }
    reverse(out.begin(), out.end());
    cout << "PREFIX_RESULT " << out << "\n";
}

// ═══════════════════════════════════════════════════════
//  2. DUPLICATE DETECTION
// ═══════════════════════════════════════════════════════
void findDuplicates(const vector<int>& arr) {
    unordered_set<int> seen;
    unordered_set<int> dups;
    cout << "DUP_STEPS\n";
    for (int x : arr) {
        if (seen.count(x)) {
            dups.insert(x);
            cout << "DUP_FOUND " << x << "\n";
        } else {
            seen.insert(x);
            cout << "DUP_CHECK " << x << "\n";
        }
    }
    cout << "DUP_STEPS_END\n";
    cout << "DUP_RESULT";
    for (int d : dups) cout << " " << d;
    cout << "\n";
}

// ═══════════════════════════════════════════════════════
//  3. GRAPH BFS + DFS
// ═══════════════════════════════════════════════════════
class Graph {
    unordered_map<int, vector<int>> adj;
public:
    void addEdge(int u, int v) {
        adj[u].push_back(v);
        adj[v].push_back(u);
    }
    void printEdges() {
        set<pair<int,int>> done;
        cout << "GRAPH_EDGES\n";
        for (auto& [u, nbrs] : adj)
            for (int v : nbrs)
                if (!done.count({min(u,v), max(u,v)})) {
                    cout << u << " " << v << "\n";
                    done.insert({min(u,v), max(u,v)});
                }
        cout << "GRAPH_EDGES_END\n";
    }
    void BFS(int start) {
        unordered_map<int,bool> vis;
        queue<int> q;
        vis[start] = true; q.push(start);
        cout << "BFS_START " << start << "\n";
        while (!q.empty()) {
            int n = q.front(); q.pop();
            cout << "VISIT " << n << "\n";
            for (int nb : adj[n])
                if (!vis[nb]) { vis[nb]=true; cout<<"EDGE "<<n<<" "<<nb<<"\n"; q.push(nb); }
        }
        cout << "BFS_END\n";
    }
    void DFS(int start) {
        unordered_map<int,bool> vis;
        stack<int> s; s.push(start);
        cout << "DFS_START " << start << "\n";
        while (!s.empty()) {
            int n = s.top(); s.pop();
            if (vis[n]) continue;
            vis[n] = true;
            cout << "VISIT " << n << "\n";
            for (int nb : adj[n])
                if (!vis[nb]) { cout<<"EDGE "<<n<<" "<<nb<<"\n"; s.push(nb); }
        }
        cout << "DFS_END\n";
    }
};

// ═══════════════════════════════════════════════════════
//  MAIN
// ═══════════════════════════════════════════════════════
int main() {
    // Expression
    string expr = "A+B*(C-D)/E";
    cout << "EXPR_INPUT " << expr << "\n";
    infixToPostfix(expr);
    infixToPrefix(expr);

    // Duplicates
    vector<int> arr = {4, 2, 7, 2, 9, 4, 1, 7, 3};
    cout << "DUP_INPUT";
    for (int x : arr) cout << " " << x;
    cout << "\n";
    findDuplicates(arr);

    // Graph
    Graph g;
    g.addEdge(0,1); g.addEdge(0,2);
    g.addEdge(1,3); g.addEdge(1,4);
    g.addEdge(2,5); g.addEdge(2,6);
    g.printEdges();
    g.BFS(0);
    g.DFS(0);

    return 0;
}
