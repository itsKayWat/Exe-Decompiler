import os
import sys
import subprocess
import shutil
import json
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import winreg
import platform
import ctypes
import tempfile
import re

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

class ElectronAnalyzer:
    def __init__(self):
        try:
            # Get script directory
            if getattr(sys, 'frozen', False):
                self.script_dir = os.path.dirname(sys.executable)
            else:
                self.script_dir = os.path.dirname(os.path.abspath(__file__))
            
            # Initialize paths
            self.app_path = None
            self.output_dir = None
            self.npm_path = None
            
            # Modern Dark Theme Colors
            self.colors = {
                'bg': '#1a1a1a',           # Main background
                'fg': '#ffffff',           # Text color
                'button_bg': '#2d2d2d',    # Button background
                'button_hover': '#3d3d3d', # Button hover
                'accent': '#4a9eff',       # Accent color (subtle blue)
                'frame_bg': '#202020',     # Frame background
                'console_bg': '#000000',   # Console background
                'console_fg': '#4a9eff',   # Console text
                'error': '#ff4a4a',        # Error messages
                'success': '#4aff4a'       # Success messages
            }
            
            # Initialize root with dark theme
            self.root = tk.Tk()
            self.root.title("Electron Decompiler")
            self.root.geometry("800x600")
            self.root.configure(bg=self.colors['bg'])
            
            # Configure styles
            self.configure_styles()
            
            # Setup UI
            self.setup_ui()
            
            # Find NPM
            self.find_and_setup_npm()
            
            self.extracted_files = []
            self.modified_files = set()
            
        except Exception as e:
            messagebox.showerror("Initialization Error", f"Error during startup: {str(e)}")
            raise

    def configure_styles(self):
        """Configure modern dark theme styles"""
        style = ttk.Style()
        style.theme_use('clam')  # Use clam theme as base
        
        # Configure frame style
        style.configure('Dark.TFrame',
                       background=self.colors['frame_bg'])
        
        # Configure label style
        style.configure('Dark.TLabel',
                       background=self.colors['frame_bg'],
                       foreground=self.colors['fg'])
        
        # Configure button style
        style.configure('Dark.TButton',
                       background=self.colors['button_bg'],
                       foreground=self.colors['fg'],
                       borderwidth=0,
                       focuscolor=self.colors['accent'],
                       lightcolor=self.colors['button_bg'],
                       darkcolor=self.colors['button_bg'],
                       relief='flat')
        
        style.map('Dark.TButton',
                 background=[('active', self.colors['button_hover'])])
        
        # Configure labelframe style
        style.configure('Dark.TLabelframe',
                       background=self.colors['frame_bg'],
                       foreground=self.colors['fg'],
                       bordercolor=self.colors['button_bg'])
        
        style.configure('Dark.TLabelframe.Label',
                       background=self.colors['frame_bg'],
                       foreground=self.colors['accent'])

    def setup_ui(self):
        """Setup modern dark themed UI"""
        # Configure menu style
        self.root.option_add('*Menu.background', self.colors['button_bg'])
        self.root.option_add('*Menu.foreground', self.colors['fg'])
        self.root.option_add('*Menu.selectColor', self.colors['accent'])
        
        # Menu bar with dark theme
        menubar = tk.Menu(self.root, bg=self.colors['button_bg'], fg=self.colors['fg'])
        self.root.config(menu=menubar)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0, bg=self.colors['button_bg'], fg=self.colors['fg'])
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Instructions", command=self.show_instructions)
        
        # Main frame
        main_frame = ttk.Frame(self.root, style='Dark.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # App selection frame
        app_frame = ttk.LabelFrame(main_frame, text="Application Selection", style='Dark.TLabelframe')
        app_frame.pack(fill=tk.X, pady=5)
        
        self.app_path_var = tk.StringVar()
        entry = tk.Entry(app_frame, 
                        textvariable=self.app_path_var,
                        bg=self.colors['button_bg'],
                        fg=self.colors['fg'],
                        insertbackground=self.colors['fg'])
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        browse_btn = ttk.Button(app_frame, 
                              text="Browse",
                              command=self.browse_app,
                              style='Dark.TButton')
        browse_btn.pack(side=tk.LEFT)
        
        # Tools frame
        tools_frame = ttk.LabelFrame(main_frame, text="Tools Installation", style='Dark.TLabelframe')
        tools_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(tools_frame,
                  text="Install Required Tools",
                  command=self.install_tools,
                  style='Dark.TButton').pack(fill=tk.X, padx=5, pady=5)
        
        # Analysis frame
        analysis_frame = ttk.LabelFrame(main_frame, text="Analysis Options", style='Dark.TLabelframe')
        analysis_frame.pack(fill=tk.X, pady=5)
        
        for text, cmd in [
            ("Extract ASAR", self.extract_asar),
            ("Analyze Source Maps", self.analyze_source_maps),
            ("Setup DevTools", self.setup_devtools)
        ]:
            ttk.Button(analysis_frame,
                      text=text,
                      command=cmd,
                      style='Dark.TButton').pack(fill=tk.X, padx=5, pady=2)
        
        # Modification frame
        mod_frame = ttk.LabelFrame(main_frame, text="Modification Options", style='Dark.TLabelframe')
        mod_frame.pack(fill=tk.X, pady=5)
        
        for text, cmd in [
            ("Edit Files", self.edit_files),
            ("Recompile Changes", self.recompile_changes)
        ]:
            ttk.Button(mod_frame,
                      text=text,
                      command=cmd,
                      style='Dark.TButton').pack(fill=tk.X, padx=5, pady=2)
        
        # Console frame
        console_frame = ttk.LabelFrame(main_frame, text="Console Output", style='Dark.TLabelframe')
        console_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.console = tk.Text(console_frame,
                             bg=self.colors['console_bg'],
                             fg=self.colors['console_fg'],
                             insertbackground=self.colors['fg'],
                             relief='flat',
                             padx=5,
                             pady=5)
        self.console.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def log(self, message):
        """Add message to console"""
        if hasattr(self, 'console'):
            self.console.insert(tk.END, f"{message}\n")
            self.console.see(tk.END)
            self.root.update()
        else:
            print(message)  # Fallback if console isn't ready

    def find_and_setup_npm(self):
        """Find NPM and set it up"""
        try:
            # Check common Node.js installation paths
            possible_paths = [
                r"C:\Program Files\nodejs\npm.cmd",
                r"C:\Program Files (x86)\nodejs\npm.cmd",
                os.path.expandvars(r"%APPDATA%\npm\npm.cmd"),
                os.path.expandvars(r"%ProgramFiles%\nodejs\npm.cmd"),
                os.path.expandvars(r"%ProgramFiles(x86)%\nodejs\npm.cmd")
            ]
            
            # Try to find npm in PATH first
            try:
                result = subprocess.run("where npm.cmd", shell=True, 
                                     capture_output=True, text=True)
                if result.returncode == 0:
                    self.npm_path = result.stdout.strip()
                    self.log(f"Found NPM at: {self.npm_path}")
                    return
            except:
                pass
            
            # Try registry
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                                  r"SOFTWARE\Node.js", 0, 
                                  winreg.KEY_READ | winreg.KEY_WOW64_64KEY) as key:
                    nodejs_path = winreg.QueryValueEx(key, "InstallPath")[0]
                    npm_path = os.path.join(nodejs_path, "npm.cmd")
                    if os.path.exists(npm_path):
                        self.npm_path = npm_path
                        self.log(f"Found NPM at: {self.npm_path}")
                        return
            except:
                pass
            
            # Try common paths
            for path in possible_paths:
                if os.path.exists(path):
                    self.npm_path = path
                    self.log(f"Found NPM at: {self.npm_path}")
                    return
            
            self.log("NPM not found. Please install Node.js from https://nodejs.org/")
            
        except Exception as e:
            self.log(f"Error finding NPM: {str(e)}")

    def browse_app(self):
        """Browse for Electron executable"""
        try:
            path = filedialog.askopenfilename(
                title="Select Electron Executable",
                filetypes=[("Executable files", "*.exe"), ("All files", "*.*")]
            )
            if path:
                # Get the parent directory containing the .exe
                app_dir = os.path.dirname(path)
                # Create output directory next to script using exe name without extension
                app_name = os.path.splitext(os.path.basename(path))[0]
                self.output_dir = os.path.join(self.script_dir, app_name)
                os.makedirs(self.output_dir, exist_ok=True)
                
                self.app_path = app_dir
                self.app_path_var.set(path)
                self.log(f"Selected application: {path}")
                self.log(f"Working directory: {self.output_dir}")
                
        except Exception as e:
            self.log(f"Error selecting application: {str(e)}")

    def install_tools(self):
        """Install required npm packages"""
        if not self.npm_path:
            msg = ("NPM not found. Please install Node.js from:\n"
                  "https://nodejs.org/en/download/\n"
                  "and restart this application.")
            messagebox.showerror("Error", msg)
            return
            
        tools = [
            'electron-fiddle',
            'asar',
            'source-map-explorer',
            'electron-devtools-installer',
            'electron-debug',
            'devtron'
        ]
        
        for tool in tools:
            try:
                self.log(f"Installing {tool}...")
                # Use full path to npm.cmd and run with shell=True
                cmd = f'"{self.npm_path}" install -g {tool}'
                process = subprocess.run(cmd, shell=True, 
                                      capture_output=True, text=True)
                
                if process.returncode == 0:
                    self.log(f"Successfully installed {tool}")
                else:
                    self.log(f"Error installing {tool}: {process.stderr}")
                    
            except Exception as e:
                self.log(f"Error installing {tool}: {str(e)}")
                
        self.log("\nAll tools installation completed.")
        
    def extract_asar(self):
        """Extract ASAR archive"""
        if not self.app_path:
            messagebox.showerror("Error", "Please select an application first")
            return
            
        if not self.npm_path:
            messagebox.showerror("Error", "NPM not found. Please install Node.js first")
            return
            
        try:
            self.log("\nSearching for ASAR files...")
            found_asar = False
            
            # First check if the selected path is itself an ASAR file
            if self.app_path.endswith('.asar'):
                found_asar = True
                if self.extract_single_asar(self.app_path):
                    return True
            
            # Get the actual application directory (parent of the .exe)
            app_dir = os.path.dirname(self.app_path)
            self.log(f"Searching in application directory: {app_dir}")
            
            # Expanded list of common locations relative to the .exe location
            common_paths = [
                os.path.join(app_dir, 'resources', 'app.asar'),
                os.path.join(app_dir, 'resources', 'default_app.asar'),
                os.path.join(app_dir, 'app.asar'),
                os.path.join(app_dir, 'resources', 'app', 'app.asar'),
                os.path.join(app_dir, 'Contents', 'Resources', 'app.asar'),
                os.path.join(app_dir, 'Contents', 'Resources', 'default_app.asar'),
                os.path.join(app_dir, 'resources', 'electron.asar'),
                os.path.join(app_dir, 'resources', 'default_app', 'app.asar'),
                # Add parent directory locations
                os.path.join(os.path.dirname(app_dir), 'resources', 'app.asar'),
                os.path.join(os.path.dirname(app_dir), 'app.asar')
            ]
            
            # First check common locations
            for asar_path in common_paths:
                if os.path.exists(asar_path):
                    found_asar = True
                    self.log(f"\nFound ASAR: {asar_path}")
                    if self.extract_single_asar(asar_path):
                        return True
            
            # If no ASAR found in common locations, do a deep search
            if not found_asar:
                self.log("No ASAR found in common locations. Performing deep search...")
                # Search up to 2 parent directories
                search_dirs = [
                    app_dir,
                    os.path.dirname(app_dir),
                    os.path.dirname(os.path.dirname(app_dir))
                ]
                
                for search_dir in search_dirs:
                    self.log(f"Searching in: {search_dir}")
                    for root, _, files in os.walk(search_dir):
                        for file in files:
                            if file.endswith('.asar'):
                                found_asar = True
                                asar_path = os.path.join(root, file)
                                self.log(f"\nFound ASAR: {asar_path}")
                                if self.extract_single_asar(asar_path):
                                    return True
            
            # Handle unpacked resources if no ASAR found
            if not found_asar:
                self.log("\nNo ASAR files found. Looking for unpacked resources...")
                if self.handle_unpacked_resources(app_dir):
                    return True
                
                self.log("\nTrying alternative extraction methods...")
                # Try to find and extract any packed JavaScript files
                if self.extract_packed_js(app_dir):
                    return True
            
            self.log("\nNo extractable resources found.")
            messagebox.showwarning("Warning", 
                                 "Could not find any ASAR files or resources to extract.\n"
                                 "The application might be using a different packaging method.")
            
        except Exception as e:
            self.log(f"Error during extraction process: {str(e)}")
            messagebox.showerror("Error", f"Extraction failed: {str(e)}")
            return False

    def extract_single_asar(self, asar_path):
        """Extract a single ASAR file"""
        try:
            # Create unique extraction directory based on ASAR name
            asar_name = os.path.splitext(os.path.basename(asar_path))[0]
            extract_dir = os.path.join(self.output_dir, f'extracted_{asar_name}')
            os.makedirs(extract_dir, exist_ok=True)
            
            # Try multiple extraction methods
            methods = [
                # Method 1: npm exec asar
                lambda: subprocess.run(
                    f'"{self.npm_path}" exec asar extract "{asar_path}" "{extract_dir}"',
                    shell=True, capture_output=True, text=True
                ),
                # Method 2: global asar
                lambda: subprocess.run(
                    f'asar extract "{asar_path}" "{extract_dir}"',
                    shell=True, capture_output=True, text=True
                ),
                # Method 3: npx asar
                lambda: subprocess.run(
                    f'"{self.npm_path}" exec --yes asar extract "{asar_path}" "{extract_dir}"',
                    shell=True, capture_output=True, text=True
                )
            ]
            
            for method in methods:
                try:
                    result = method()
                    if result.returncode == 0:
                        self.log(f"Successfully extracted to: {extract_dir}")
                        self.extracted_files = self.get_extracted_files(extract_dir)
                        self.modified_files = set()
                        os.startfile(extract_dir)
                        return True
                except Exception as e:
                    self.log(f"Method failed: {str(e)}")
                    continue
                
            self.log("All extraction methods failed")
            return False
            
        except Exception as e:
            self.log(f"Error extracting {asar_path}: {str(e)}")
            return False

    def handle_unpacked_resources(self, directory):
        """Handle cases where no ASAR files are found"""
        self.log("\nNo ASAR files found. Checking for unpacked resources...")
        
        # List of common resource directories
        resource_dirs = [
            os.path.join(directory, 'resources'),
            os.path.join(directory, 'Resources'),
            os.path.join(directory, 'app'),
            os.path.join(directory, 'resources', 'app'),
            os.path.join(directory, 'Contents', 'Resources')
        ]
        
        found = False
        for res_dir in resource_dirs:
            if os.path.exists(res_dir):
                found = True
                self.log(f"Found resources directory: {res_dir}")
                try:
                    dest_dir = os.path.join(self.output_dir, 'resources')
                    shutil.copytree(res_dir, dest_dir, dirs_exist_ok=True)
                    self.log(f"Copied resources to: {dest_dir}")
                    self.extracted_files = self.get_extracted_files(dest_dir)
                    self.modified_files = set()
                    os.startfile(dest_dir)
                    break
                except Exception as e:
                    self.log(f"Error copying resources: {str(e)}")
                
        if not found:
            self.log("No resources directory found")
            messagebox.showwarning("Warning", 
                                 "No ASAR files or resources directory found.")

    def get_extracted_files(self, directory):
        """Recursively get all files in extracted directory"""
        files = []
        for root, _, filenames in os.walk(directory):
            for filename in filenames:
                files.append(os.path.join(root, filename))
        return files

    def analyze_source_maps(self):
        """Analyze source maps if available"""
        if not self.output_dir:
            messagebox.showerror("Error", "Please extract ASAR first")
            return
            
        try:
            # Look for .js.map files
            for root, _, files in os.walk(self.output_dir):
                for file in files:
                    if file.endswith('.js.map'):
                        map_path = os.path.join(root, file)
                        js_path = map_path[:-4]  # Remove .map extension
                        if os.path.exists(js_path):
                            self.log(f"\nAnalyzing source map: {file}")
                            subprocess.run(['source-map-explorer', js_path], check=True)
                            
        except subprocess.CalledProcessError as e:
            self.log(f"Error analyzing source maps: {str(e)}")
            
    def setup_devtools(self):
        """Setup development tools"""
        if not self.output_dir:
            messagebox.showerror("Error", "Please extract ASAR first")
            return
            
        try:
            # Create a development config
            dev_config = {
                "devTools": True,
                "openDevTools": True,
                "devtron": True,
                "sourceMapSupport": True
            }
            
            config_path = os.path.join(self.output_dir, 'dev-config.json')
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            
            with open(config_path, 'w') as f:
                json.dump(dev_config, f, indent=2)
                
            self.log("\nDevelopment configuration created:")
            self.log(f"Config saved to: {config_path}")
            self.log("Add these settings to your main process file to enable DevTools")
            
        except Exception as e:
            self.log(f"Error setting up DevTools: {str(e)}")
            
    def edit_files(self):
        """Open file browser to edit extracted files"""
        if not self.output_dir or not os.path.exists(self.output_dir):
            messagebox.showerror("Error", "Please extract the application first")
            return
            
        try:
            # Show exact path being opened
            self.log(f"\nOpening directory: {self.output_dir}")
            self.log("Look for these key files:")
            self.log("- main.js (main process code)")
            self.log("- renderer.js (renderer process code)")
            self.log("- index.html (main window)")
            self.log("- package.json (application config)")
            
            # Open file explorer to the exact directory
            os.startfile(self.output_dir)
            
            self.log("\nEditing Instructions:")
            self.log("1. Navigate to the file you want to modify")
            self.log("2. Make your changes using any text editor")
            self.log("3. Save your changes")
            self.log("4. Click 'Recompile Changes' when done")
            
        except Exception as e:
            self.log(f"Error opening editor: {str(e)}")
            
    def recompile_changes(self):
        """Recompile modified files back into ASAR"""
        if not self.output_dir or not os.path.exists(self.output_dir):
            messagebox.showerror("Error", "No files to recompile")
            return
            
        try:
            self.log("\nPreparing to recompile changes...")
            
            # Find all potential ASAR locations
            asar_locations = [
                os.path.join(self.app_path, 'resources', 'app.asar'),
                os.path.join(self.app_path, 'resources', 'default_app.asar'),
                os.path.join(self.app_path, 'app.asar')
            ]
            
            original_asars = [path for path in asar_locations if os.path.exists(path)]
            
            if not original_asars:
                self.log("Warning: Could not find original ASAR file")
                # Ask user where to save the new ASAR
                save_path = filedialog.asksaveasfilename(
                    defaultextension=".asar",
                    filetypes=[("ASAR files", "*.asar"), ("All files", "*.*")],
                    title="Save Recompiled ASAR As"
                )
                if not save_path:
                    return
                original_asars = [save_path]
            
            for original_asar in original_asars:
                try:
                    # Create backup
                    backup_path = original_asar + '.backup'
                    if os.path.exists(original_asar):
                        shutil.copy2(original_asar, backup_path)
                        self.log(f"Created backup at: {backup_path}")
                    
                    # Pack modified files
                    new_asar = os.path.join(self.output_dir, 'app.asar')
                    self.log(f"Creating new ASAR at: {new_asar}")
                    
                    # Try multiple packing methods
                    pack_methods = [
                        f'"{self.npm_path}" exec asar pack "{self.output_dir}" "{new_asar}"',
                        f'asar pack "{self.output_dir}" "{new_asar}"',
                        f'"{self.npm_path}" exec --yes asar pack "{self.output_dir}" "{new_asar}"'
                    ]
                    
                    success = False
                    for cmd in pack_methods:
                        try:
                            self.log(f"Trying: {cmd}")
                            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                            if result.returncode == 0:
                                success = True
                                break
                        except Exception as e:
                            self.log(f"Method failed: {str(e)}")
                    
                    if not success:
                        raise Exception("All packing methods failed")
                    
                    self.log("Successfully created new ASAR")
                    
                    # Try to replace original ASAR with elevated privileges
                    if os.path.exists(original_asar):
                        if self.replace_asar(new_asar, original_asar):
                            self.log("Successfully replaced original ASAR")
                            messagebox.showinfo("Success", 
                                              "Changes have been recompiled and applied.\n"
                                              f"Original file replaced at:\n{original_asar}")
                            return True
                        
                except Exception as e:
                    self.log(f"Error processing {original_asar}: {str(e)}")
                    
            raise Exception("Failed to replace any ASAR files")
            
        except Exception as e:
            self.log(f"Error during recompilation: {str(e)}")
            messagebox.showerror("Error", f"Recompilation failed: {str(e)}")
            return False

    def replace_asar(self, new_asar, original_asar):
        """Try multiple methods to replace the original ASAR file"""
        methods = [
            # Method 1: Direct replacement
            lambda: os.replace(new_asar, original_asar),
            
            # Method 2: Take ownership and set permissions
            lambda: self.take_ownership_and_replace(new_asar, original_asar),
            
            # Method 3: PowerShell elevated copy
            lambda: subprocess.run(
                f'powershell Start-Process cmd -Verb RunAs -ArgumentList "/c copy /Y \\"{new_asar}\\" \\"{original_asar}\\""',
                shell=True
            )
        ]
        
        for method in methods:
            try:
                method()
                if os.path.exists(original_asar):
                    return True
            except Exception as e:
                self.log(f"Replacement method failed: {str(e)}")
                continue
            
        return False

    def take_ownership_and_replace(self, new_asar, original_asar):
        """Take ownership of file and replace it"""
        subprocess.run(['takeown', '/F', original_asar], shell=True, check=True)
        subprocess.run(['icacls', original_asar, '/grant', 'administrators:F'], shell=True, check=True)
        os.replace(new_asar, original_asar)

    def show_instructions(self):
        """Show readme/instructions window"""
        readme = tk.Toplevel(self.root)
        readme.title("Instructions")
        readme.geometry("600x400")
        readme.configure(bg=self.colors['bg'])
        
        text = tk.Text(readme,
                      wrap=tk.WORD,
                      padx=10,
                      pady=10,
                      bg=self.colors['console_bg'],
                      fg=self.colors['fg'],
                      insertbackground=self.colors['fg'])
        text.pack(fill=tk.BOTH, expand=True)
        
        instructions = """
Electron App Decompiler Instructions
==================================

Prerequisites:
-------------
1. Install Node.js from https://nodejs.org/
2. Run as Administrator
3. Click "Install Required Tools" before first use

Step-by-Step Guide:
------------------
1. Application Selection:
   - Click "Browse" to select your Electron .exe file
   - The working directory will be created next to this script

2. Tools Installation:
   - Click "Install Required Tools" to set up required npm packages
   - Wait for all tools to install successfully

3. Analysis Options:
   - Click "Extract ASAR" to decompile the application
   - Files will be extracted to: [script_directory]/[app_name]/
   - "Analyze Source Maps" helps understand the code structure
   - "Setup DevTools" enables development tools

4. Making Modifications:
   - Click "Edit Files" to open the extracted files
   - Make your changes to the files using any text editor
   - Common files to modify:
     * main.js (main process code)
     * renderer.js (renderer process code)
     * index.html (main window)
     * package.json (application config)

5. Recompiling:
   - After making changes, click "Recompile Changes"
   - This will pack your modifications back into the ASAR
   - The original file will be backed up with .backup extension
   - Administrator rights are needed to replace the original file

Troubleshooting:
---------------
- If NPM is not found: Install Node.js and restart the application
- If extraction fails: Check application directory structure
- If recompile fails: Run as administrator
- Check console output for detailed error messages

Notes:
------
- Always make a backup before modifying applications
- Some applications may have additional protection
- Modifications might break application functionality
- Check console output for detailed progress and errors
"""
        
        text.insert('1.0', instructions)
        text.config(state='disabled')
        
        # Themed scrollbar
        scrollbar = ttk.Scrollbar(readme, orient='vertical', command=text.yview)
        scrollbar.pack(side='right', fill='y')
        text.config(yscrollcommand=scrollbar.set)
        
        # Themed close button
        close_btn = ttk.Button(readme, text="Close", command=readme.destroy)
        close_btn.pack(pady=5)

    def extract_packed_js(self, directory):
        """Try to find and extract packed JavaScript files"""
        try:
            js_files = []
            for root, _, files in os.walk(directory):
                for file in files:
                    if file.endswith('.js'):
                        js_files.append(os.path.join(root, file))
            
            if not js_files:
                return False
            
            # Create extraction directory
            extract_dir = os.path.join(self.output_dir, 'extracted_js')
            os.makedirs(extract_dir, exist_ok=True)
            
            found_content = False
            for js_file in js_files:
                try:
                    # Copy the file to extraction directory
                    dest_file = os.path.join(extract_dir, os.path.basename(js_file))
                    shutil.copy2(js_file, dest_file)
                    found_content = True
                    self.log(f"Copied JavaScript file: {os.path.basename(js_file)}")
                except Exception as e:
                    self.log(f"Error copying {js_file}: {str(e)}")
            
            if found_content:
                self.log(f"\nExtracted JavaScript files to: {extract_dir}")
                self.extracted_files = self.get_extracted_files(extract_dir)
                self.modified_files = set()
                os.startfile(extract_dir)
                return True
            
            return False
            
        except Exception as e:
            self.log(f"Error extracting JavaScript files: {str(e)}")
            return False

    def run(self):
        """Start the application"""
        try:
            self.root.mainloop()
        except Exception as e:
            messagebox.showerror("Runtime Error", f"Error during execution: {str(e)}")
            raise

def main():
    """Main entry point for the application"""
    try:
        # Run the application
        app = ElectronAnalyzer()
        app.run()
    except Exception as e:
        print(f"Startup error: {str(e)}")
        input("Press Enter to exit...")  # Keep window open on error
        sys.exit(1)

if __name__ == "__main__":
    main()
