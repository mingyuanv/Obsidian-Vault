import subprocess
import sys
import os
import platform
import datetime
import argparse

if platform.system() == "Windows":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

class SilentGitSync:
    def __init__(self):
        self.git_cmd = "git"
        self._setup_platform()
        self._disguise_process()
        
    def _setup_platform(self):
        if platform.system() == "Windows":
            self.startupinfo = subprocess.STARTUPINFO()
            self.startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            self.creationflags = subprocess.CREATE_NO_WINDOW
        else:
            self.startupinfo = None
            self.creationflags = 0
            
    def _disguise_process(self):
        try:
            if platform.system() == "Linux":
                import ctypes
                libc = ctypes.CDLL(None)
                libc.prctl(15, b"system-sync", 0, 0, 0)
            elif platform.system() == "Darwin":
                import ctypes
                libc = ctypes.CDLL(None)
                libc.setprogname(b"system-sync")
        except:
            pass
            
    def _is_git_repo(self, path):
        git_dir = os.path.join(path, ".git")
        return os.path.exists(git_dir) and os.path.isdir(git_dir)
    
    def _has_changes(self, repo_path):
        status, stdout, stderr = self._run_git_command([self.git_cmd, "status", "--porcelain"], repo_path)
        return status == 0 and len(stdout) > 0
        
    def _run_git_command(self, args, cwd):
        try:
            process = subprocess.Popen(
                args,
                shell=False,
                cwd=cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8',
                startupinfo=self.startupinfo,
                creationflags=self.creationflags
            )
            
            stdout, stderr = process.communicate(timeout=120)
            return process.returncode, stdout.strip(), stderr.strip()
        except subprocess.TimeoutExpired:
            return -1, "", "Command timeout"
        except Exception as e:
            return -1, "", str(e)
            
    def sync_repo(self, repo_path, repo_name, do_push=True, force=False):
        if not os.path.exists(repo_path):
            return False, f"路径不存在"
            
        if not self._is_git_repo(repo_path):
            return False, f"不是Git仓库"
            
        if not force and not self._has_changes(repo_path):
            return True, "无变更需提交"
            
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        commit_msg = f"Auto sync at {timestamp}"
        
        status, stdout, stderr = self._run_git_command([self.git_cmd, "add", "."], repo_path)
        if status != 0 and stderr:
            return False, f"[add] {stderr}"
            
        status, stdout, stderr = self._run_git_command([self.git_cmd, "commit", "-m", commit_msg], repo_path)
        if status != 0:
            return False, f"[commit] {stderr}"
            
        if do_push:
            status, stdout, stderr = self._run_git_command([self.git_cmd, "push"], repo_path)
            if status != 0:
                return False, f"[push] {stderr}"
            return True, "提交并推送成功"
        else:
            return True, "仅提交成功（未推送）"
        
    def sync_all(self, repos, do_push=True, repo_names=None):
        results = []
        
        if repo_names:
            target_repos = {name: path for name, path in repos.items() if name in repo_names}
        else:
            target_repos = repos
            
        for repo_name, repo_path in target_repos.items():
            success, message = self.sync_repo(repo_path, repo_name, do_push)
            results.append({
                "repo": repo_name,
                "success": success,
                "message": message
            })
        return results

def main():
    parser = argparse.ArgumentParser(description="多仓库Git同步工具（进程伪装版）")
    parser.add_argument("-p", "--push", action="store_true", help="推送至远程仓库（默认仅提交，不推送）")
    parser.add_argument("-l", "--list", action="store_true", help="列出所有配置的仓库")
    parser.add_argument("-v", "--verbose", action="store_true", help="显示详细输出")
    parser.add_argument("-r", "--repo", type=str, help="指定单个仓库名称，如: -r 主库")
    parser.add_argument("-f", "--force", action="store_true", help="强制提交（即使无变更）")
    args = parser.parse_args()
    
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
        tools_dir = base_path
    else:
        script_path = os.path.abspath(__file__)
        tools_dir = os.path.dirname(script_path)
        base_path = os.path.dirname(tools_dir)
    
    repos = {
        "主库": base_path,
        "Extended-Learn": os.path.join(base_path, "Extended-Learn"),
        "XGRIDS": os.path.join(base_path, "XGRIDS"),
        "code-notes": os.path.join(base_path, "功能子仓库", "code-notes"),
        "develop-skills": os.path.join(base_path, "功能子仓库", "develop-skills"),
        "large-files": os.path.join(base_path, "功能子仓库", "large-files")
    }
    
    if args.list:
        print("Repositories configured:")
        for name, path in repos.items():
            is_git = "OK" if os.path.exists(os.path.join(path, ".git")) else "NO"
            has_change = "有变更" if os.path.exists(os.path.join(path, ".git")) and SilentGitSync()._has_changes(path) else "无变更"
            print(f"  [{is_git}] {name}: {path} ({has_change})")
        return
        
    target_repos = None
    if args.repo:
        if args.repo in repos:
            target_repos = [args.repo]
        else:
            print(f"错误：仓库 '{args.repo}' 不存在")
            print("可用仓库: " + ", ".join(repos.keys()))
            return
        
    sync = SilentGitSync()
    results = sync.sync_all(repos, do_push=args.push, repo_names=target_repos)
    
    if args.verbose:
        print("\n同步结果：")
        for result in results:
            status = "✓" if result["success"] else "✗"
            print(f"  {status} {result['repo']}: {result['message']}")
    
    log_path = os.path.join(tools_dir, "sync_log.txt")
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"\n=== {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")
        f.write(f"模式: {'提交+推送' if args.push else '仅提交'}\n")
        f.write(f"目标: {'全部仓库' if not target_repos else ','.join(target_repos)}\n")
        for result in results:
            status = "✓" if result["success"] else "✗"
            log_line = f"{status} {result['repo']}: {result['message']}"
            f.write(log_line + "\n")

if __name__ == "__main__":
    main()