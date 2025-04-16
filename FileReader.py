class Reader:
    def __init__(self, path):
        self.path = path
        self.ScanFile()

        if self.has_content:
            print("Scan Successful.")
        else:
            print(f"HARD ERROR: {self.error}.")
            del self
        
    
    def ScanFile(self):
        try:
            with open(self.path, "r") as f:
                self.lines = [l.strip() for l in f.readlines() if l.strip()]
                self.lcount = len(self.lines)
                self.has_content = self.lcount > 0
                if not self.has_content:
                    self.error = "File empty"
                return
            
        except FileNotFoundError as e:
            self.lines = None
            self.lcount = None
            self.has_content = False
            self.error = f"Console ({self.path}) does not exist"
            return
            
        except Exception as e:
            self.lines = None
            self.lcount = None
            self.has_content = False
            self.error = e
            return
        

if __name__ == "__main__":
    r = Reader("console.txt")
    print(r.lines)