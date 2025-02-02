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
        """Browse for Electron application"""
        try:
            path = filedialog.askdirectory(title="Select Electron Application Directory")
            if path:
                # Create output directory next to script using target app name
                app_name = os.path.basename(path)
                self.output_dir = os.path.join(self.script_dir, app_name)
                os.makedirs(self.output_dir, exist_ok=True)
                
                self.app_path = path
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
            
            # First check common locations
            common_paths = [
                os.path.join(self.app_path, 'resources', 'app.asar'),
                os.path.join(self.app_path, 'resources', 'default_app.asar'),
                os.path.join(self.app_path, 'app.asar')
            ]
            
            for asar_path in common_paths:
                if os.path.exists(asar_path):
                    found_asar = True
                    self.log(f"\nFound ASAR: {asar_path}")
                    
                    # Create extraction directory
                    extract_dir = os.path.join(self.output_dir, 'extracted_asar')
                    os.makedirs(extract_dir, exist_ok=True)
                    
                    # Try extraction methods
                    try:
                        # Method 1: Using npm exec asar
                        self.log("Attempting extraction with npm exec asar...")
                        cmd = f'"{self.npm_path}" exec asar extract "{asar_path}" "{extract_dir}"'
                        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                        
                        if result.returncode != 0:
                            # Method 2: Using global asar
                            self.log("Trying alternative extraction method...")
                            cmd = f'asar extract "{asar_path}" "{extract_dir}"'
                            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                        
                        if result.returncode == 0:
                            self.log(f"Successfully extracted to: {extract_dir}")
                            # Open the directory
                            os.startfile(extract_dir)
                            self.extracted_files = [os.path.join(extract_dir, f) for f in os.listdir(extract_dir)]
                            self.modified_files = set()
                            return
                        else:
                            self.log(f"Extraction failed: {result.stderr}")
                            
                    except Exception as e:
                        self.log(f"Error during extraction: {str(e)}")
            
            # If no ASAR found in common locations, search entire directory
            if not found_asar:
                self.log("Searching entire directory for ASAR files...")
                for root, _, files in os.walk(self.app_path):
                    for file in files:
                        if file.endswith('.asar'):
                            found_asar = True
                            asar_path = os.path.join(root, file)
                            self.log(f"\nFound ASAR: {asar_path}")
                            
                            # Create extraction directory
                            extract_dir = os.path.join(self.output_dir, 
                                                     os.path.splitext(file)[0])
                            os.makedirs(extract_dir, exist_ok=True)
                            
                            try:
                                cmd = f'"{self.npm_path}" exec asar extract "{asar_path}" "{extract_dir}"'
                                self.log(f"Running: {cmd}")
                                
                                result = subprocess.run(cmd, shell=True, 
                                                     capture_output=True, text=True)
                                
                                if result.returncode == 0:
                                    self.log(f"Successfully extracted to: {extract_dir}")
                                    os.startfile(extract_dir)
                                    self.extracted_files = [os.path.join(extract_dir, f) for f in os.listdir(extract_dir)]
                                    self.modified_files = set()
                                    return
                                else:
                                    self.log(f"Extraction failed: {result.stderr}")
                                    
                            except Exception as e:
                                self.log(f"Error during extraction: {str(e)}")
            
            if not found_asar:
                self.log("\nNo ASAR files found. Checking for unpacked resources...")
                resources_path = os.path.join(self.app_path, 'resources')
                if os.path.exists(resources_path):
                    self.log("Found resources directory, copying contents...")
                    shutil.copytree(resources_path, 
                                  os.path.join(self.output_dir, 'resources'), 
                                  dirs_exist_ok=True)
                    self.log(f"Copied resources to: {self.output_dir}")
                    os.startfile(self.output_dir)
                else:
                    self.log("No resources directory found")
                    messagebox.showwarning("Warning", 
                                         "No ASAR files or resources directory found.")
                    
            if found_asar:
                self.log("\nExtraction complete. You can now:")
                self.log("1. Click 'Edit Files' to modify the extracted files")
                self.log("2. Make your changes")
                self.log("3. Click 'Recompile Changes' to apply modifications")
            
        except Exception as e:
            self.log(f"Error during extraction process: {str(e)}")
            messagebox.showerror("Error", f"Extraction failed: {str(e)}")

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
            
            # Create backup of original ASAR if it exists
            original_asar = os.path.join(self.app_path, 'resources', 'app.asar')
            if os.path.exists(original_asar):
                backup_path = original_asar + '.backup'
                shutil.copy2(original_asar, backup_path)
                self.log(f"Created backup at: {backup_path}")
            
            # Pack modified files into new ASAR
            new_asar = os.path.join(self.output_dir, 'app.asar')
            self.log(f"Creating new ASAR at: {new_asar}")
            
            # Use asar to pack
            cmd = f'"{self.npm_path}" exec asar pack "{self.output_dir}" "{new_asar}"'
            self.log(f"Running command: {cmd}")
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                self.log("Successfully created new ASAR")
                
                # Try to replace original ASAR
                try:
                    if os.path.exists(original_asar):
                        self.log(f"Replacing original ASAR at: {original_asar}")
                        # Try to take ownership and set permissions
                        subprocess.run(['takeown', '/F', original_asar], shell=True)
                        subprocess.run(['icacls', original_asar, '/grant', 'administrators:F'], shell=True)
                        # Replace the file
                        os.replace(new_asar, original_asar)
                        self.log("Successfully replaced original ASAR")
                        messagebox.showinfo("Success", 
                                          "Changes have been recompiled and applied.\n"
                                          f"Original file replaced at:\n{original_asar}")
                except Exception as e:
                    self.log(f"Error replacing original: {str(e)}")
                    self.log("Trying alternative replacement method...")
                    try:
                        # Try with elevated privileges
                        cmd = f'powershell Start-Process cmd -Verb RunAs -ArgumentList "/c copy /Y \\"{new_asar}\\" \\"{original_asar}\\""'
                        subprocess.run(cmd, shell=True)
                        if os.path.exists(original_asar):
                            self.log("Successfully replaced original ASAR")
                            messagebox.showinfo("Success", 
                                              "Changes have been recompiled and applied.\n"
                                              f"Original file replaced at:\n{original_asar}")
                    except Exception as e2:
                        self.log(f"Alternative method failed: {str(e2)}")
                        messagebox.showerror("Error", 
                                           "Could not replace original file.\n"
                                           "Please replace it manually with administrator rights.")
            else:
                self.log(f"Error during recompilation: {result.stderr}")
                messagebox.showerror("Error", "Failed to recompile changes")
                
        except Exception as e:
            self.log(f"Error during recompilation: {str(e)}")
            messagebox.showerror("Error", f"Recompilation failed: {str(e)}")
            
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
   - Click "Browse" to select your Electron application folder
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