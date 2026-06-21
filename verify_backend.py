import ast
import os
import glob

def main(ctx):
    project_root = r"D:\AI-Workspace\ai trading\ai-stock-analyzer\backend"
    results = []
    
    py_files = glob.glob(os.path.join(project_root, "**", "*.py"), recursive=True)
    
    for f in sorted(py_files):
        rel = os.path.relpath(f, project_root)
        try:
            with open(f, 'r', encoding='utf-8') as fh:
                source = fh.read()
            ast.parse(source)
            results.append(f"OK: {rel}")
        except SyntaxError as e:
            results.append(f"SYNTAX ERROR in {rel}: line {e.lineno}: {e.msg}")
        except Exception as e:
            results.append(f"ERROR in {rel}: {str(e)[:80]}")
    
    return {"total": len(py_files), "results": results}
