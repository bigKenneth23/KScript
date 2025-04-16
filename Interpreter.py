from time import time

# Try to read the interpreter if you wish, i wouldnt advise it.
# I made the bastard thing and it hurts my brain


class VariableArray:
    def __init__(self):
        self.vars = {
            "pi": 3.1415926535,
            "e": 2.7182818284,
            "time": time()
        }


    def Set(self, key, val):
        self.vars[key] = val

    
    def Get(self, key):
        return self.vars.get(key)

    
    def has_var(self, var):
        return self.Get(var) != None
    

    def Delete(self, key):
        self.vars.pop(key)


class Function:
    def __init__(self, name, chunk, args):
        self.name = name
        self.chunk = chunk
        self.args = args
        self.argc = len(args)


class FunctionArray:
    def __init__(self):
        self.funcs = []
    

    def define(self, fn_name, fn_exec, fn_args):
        self.funcs.append(Function(fn_name, fn_exec, fn_args))
    

    def Get(self, name):
        for fn in self.funcs:
            if fn.name == name:
                return fn
        return False


    def Exists(self, name):
        return self.Get(name) != False    


class Processor:

    commands = [
        "SET",
        "SAY"
    ]

    ops = [
        "PWR",
        "ADD",
        "SUB",
        "MUL",
        "DIV",
        "MOD",
        "TDV"
    ]

    bools = [
        "BGR",
        "SMR",
        "EQL",
        "NEQL"
    ]

    loops = [
        "WHL",
        "FOR"
    ]


    def __init__(self, lines: list):
        self.lines = lines
        self.vars = VariableArray()
        self.custom_funcs = FunctionArray()
        
        idx = 0
        while idx < len(lines):
            stat = self.Prepline(idx)

            if not stat:
                return
            
            idx += 1
        


    def Prepline(self, idx):
        try:
            line = self.lines[idx]
        except IndexError:
            return True

        if line.strip().startswith("IF"):
            stat = self.EvalChunk(idx)

        elif line.strip().startswith("WHL") or line.strip().startswith("FOR"):
            stat = self.EvalLoop(idx)
        
        elif line.strip().startswith("FNC"):
            stat = self.EvalFunction(idx)

        else:
            stat = self.Readline(line)

        if not stat:
            print(f"Program failed at line {idx+1}.\n   -> {line}\nFail: {self.fail}")
            return False
        
        return True
    

    def Readline(self, line: str):
        if r"//" in line:
            idx = line.index(r"//")

            comment = line[idx:]

            line = line.strip(comment).strip()
            
            if not line:
                return True
        
        if line.startswith("ANNOUNCE"):
            sec = line.removeprefix("ANNOUNCE").strip()
            if sec:
                print(sec)
                return True
            else:
                self.fail = "Announcement missing argument"
                return False
            
        
        if "=" not in line:
            self.fail = "Missing '='"
            return False
        
        tmp = [i.strip() for i in line.split("=") if i.strip()]
        if len(tmp) < 2:
            self.fail = "Incomplete expression"
            return False
        
        if len(tmp) > 2:
            self.fail = "Expression overload"
            return False

        expression = tmp[1]
        exp_val = self.ExtractExpr(expression)

        if type(exp_val) == bool and not exp_val:
            return False

        command = tmp[0]
        exec = self.ExtractCommand(command, exp_val)

        if not exec:
            return False
        
        return True
   

    def ExtractExpr(self, expression):
        parts = [i.strip() for i in expression.split(":") if i.strip()]

        if self.custom_funcs.Exists(parts[0]):
            return self.ExtractFunction(parts[:])

        if len(parts) == 1:
            if parts[0] == "TIMENOW":
                return time()
            try:
                val = float(parts[0])
                return val
            
            except:
                if self.vars.has_var(parts[0]):
                    val = self.vars.Get(parts[0])
                else:
                    self.fail = f"Unrecognised var: {parts[0]}"
                    return False
                
                return val

        if len(parts) < 3:
            self.fail = "Invalid arg count."
            return False
        
        if parts[0] not in self.ops:
            self.fail = f"Unrecognised method: {parts[0]}"
            return False
        
        op = parts[0]
        vals = parts[1:]

        try:
            total = float(vals[0])
        except:
            if self.vars.has_var(vals[0]):
                total = float(self.vars.Get(vals[0]))
            else:
                self.fail = f"Unrecognised var: {vals[0]}"
                return False
            
        break_early = False
        
        for i in range(1, len(vals)):
            val = vals[i]

            try:
                val = float(val)
            except:
                if self.vars.has_var(val):
                    val = float(self.vars.Get(val))

                else:
                    if str(val) in self.ops:
                        val = self.ExtractExpr("".join(str(i) + ":" for i in vals[i:]))

                        if not val:
                            return False
                        
                        break_early = True

                    else:
                        self.fail = f"Unrecognised var: {val}"
                        return False
                
            match op:
                case "PWR":
                    total **= val
                
                case "ADD":
                    total += val
                
                case "SUB":
                    total -= val
                
                case "DIV":
                    try:
                        total /= val
                    except:
                        self.fail = f"Cannot divide {total} by {val}"
                        return False
                    
                case "MUL":
                    total *= val
                
                case "MOD":
                    total %= val

                case "TDV":
                    try:
                        total //= val
                    except:
                        self.fail = f"Cannot divide {total} by {val}"
                        return False
                
                case _:
                    self.fail = f"Unrecognised operator: {op}"
                    return False
                
            if break_early:
                break
                
        return total


    def ExtractCommand(self, command, exp_val):
        parts = [i.strip() for i in command.split() if i.strip()]
        action = parts[0]

        if len(parts) > 2:
            self.fail = "Argument overload"
            return False
        
        if len(parts) == 1:
            if action == "SAY":
                print(exp_val)
                return True
            self.fail = f"Unrecognised method: {action}"
            return False
        
        v = parts[1]

        match action:
            case "SET":
                self.vars.Set(v, exp_val)
                return True
            case _:
                self.fail = f"Unrecognised method: {action}"
                return False
        

    def ExtractCondition(self, expression):
        parts = [i.strip() for i in expression.split(":") if i.strip()]

        op = parts[0]
        if op not in self.bools:
            self.fail = f"Unrecognised conditional: {op}"
            return None
        
        if len(parts) != 3:
            self.fail = "Invalid arg count"
            return None
        
        try:
            a = float(parts[1])
        except:
            if self.vars.has_var(parts[1]):
                a = float(self.vars.Get(parts[1]))
            else:
                self.fail = f"Unrecognised var: {parts[1]}"
                return None
        
        try:
            b = float(parts[2])
        except:
            if self.vars.has_var(parts[2]):
                b = float(self.vars.Get(parts[2]))
            else:
                self.fail = f"Unrecognised var: {parts[2]}"
                return None
            
        match(op):
            case "BGR":
                return a>b
            
            case "SMR":
                return a<b
            
            case "EQL":
                return a==b
            
            case "NEQL":
                return a!=b
            
            case _:
                self.fail = f"Unrecognised conditional: {op}" # Just in case...
                return None


    def EvalChunk(self, current_idx):
        condition_line = self.lines[current_idx]
        parts = [i.strip() for i in condition_line.split() if i.strip()]

        if len(parts) > 2:
            self.fail = f"Condition args overload"
            return False
        
        if len(parts) < 2:
            self.fail = "No condition provided"
            return False
        
        if parts[0] != "IF":
            self.fail = f"Invalid condition operator"
            return False
        
        execute = self.ExtractCondition(parts[1]) 

        if execute == None:
            return False
        
        a = current_idx + 1
        if self.lines[a].strip() != "{":
            self.fail = "Expected '{' alone, not found"
            return False
        
        b = a+1
        ignore = 0
        found = False

        while b < len(self.lines):
            tar = self.lines[b]
            if tar.strip() == "{":
                ignore += 1
            
            if tar.strip() == "}":
                if ignore:
                    ignore -= 1
                else:
                    found = True
                    break
            b += 1

        if not found:
            self.fail = "Couldn't find '}' to close '{'"
            return False
        
        else_idx = b+1
        else_line = self.lines[else_idx].strip()
        has_else = else_line == "ELS"

        if has_else:
            b1 = else_idx + 1
            if self.lines[b1].strip() != "{":
                self.fail = "Expected '{' for else, not found"
                return False
            
            ignore = 0
            found = False
            b1 += 1
            while b1 < len(self.lines):
                tar = self.lines[b1]
                if tar.strip() == "{":
                    ignore += 1
                
                if tar.strip() == "}":
                    if ignore:
                        ignore -= 1
                    else:
                        found = True
                        break
                b1 += 1

            if not found:
                self.fail = "Couldn't find '}' to close '{' in else"
                return False
        

        if execute:
            del self.lines[b], self.lines[a]
            if has_else:
                del self.lines[else_idx-2:b1-1]
        else:
            chunk_len = len(self.lines[a:b+1])
            del self.lines[a:b+1]
            if has_else:
                del self.lines[b1-chunk_len], self.lines[else_idx+1-chunk_len], self.lines[else_idx-chunk_len]

        return True
    

    def EvalLoop(self, current_idx):
        init_line = [i.strip() for i in self.lines[current_idx].split("=") if i.strip()]

        if len(init_line) != 2:
            self.fail = "Loop improperly initialized"
            return False

        kw = init_line[0]
        a = current_idx + 1

        if self.lines[a].strip() != "{":
            self.fail = "Expected '{' for loop, not found."
            return False
        
        b = a+1
        ignore = 0
        found_close = False

        while b < len(self.lines):
            tar = self.lines[b].strip()

            if tar == "{":
                ignore += 1
            
            if tar == "}":
                if ignore:
                    ignore -= 1
                else:
                    found_close = True
                    break

            b += 1

        if not found_close:
            self.fail = "Couldn't find '}' to close loop"
            return False
        
        full_chunk = self.lines[a:b+1]
        exec_chunk = full_chunk[1:-1]

        if not exec_chunk:
            self.fail = "Loop cannot be empty"
            return False
        
        if kw == "WHL":
            if len(init_line) != 2:
                self.fail = f"WHL takes 2 arguments: Found {len(init_line)}"
                return False
            
            condition = init_line[1]

            valid = self.ExtractCondition(condition)

            if valid == None:
                return False
            
            current_state = self.lines

            while self.ExtractCondition(condition):
                self.lines = exec_chunk[:]

                for idx, ln in enumerate(self.lines):

                    stat = self.Prepline(idx)

                    if not stat:
                        return False
                    
            self.lines = current_state
            del self.lines[a:b+1]

            return True
        
        else:
            for_args = [i.strip() for i in init_line[1].split(",") if i.strip()]

            if len(for_args) != 3:
                self.fail = f"FOR takes 3 arguments: Found {len(for_args)}"
                return False
            
            var_field = [i.strip() for i in for_args[0].split(":") if i.strip()]
            condition = for_args[1].strip()
            step = for_args[2].strip()

            if len(var_field) != 2:
                self.fail = "For var accepts name:value only"
                return False
            
            for_var = var_field[0]

            try:
                for_var_val = float(var_field[1])
            except:
                if self.vars.has_var(var_field[1]):
                    for_var_val = self.vars.Get(var_field[1])
                else:
                    self.fail = f"Unrecognised var: {var_field[1]}"
                    return False
            
            self.vars.Set(for_var, for_var_val)

            valid = self.ExtractCondition(condition)
            if valid == None:
                return False
            
            if step not in ["++", "--"]:
                self.fail = f"Unrecognised var step: {step}"
                return False
            
            for_step = 1 if step == "++" else -1

            current_state = self.lines

            while self.ExtractCondition(condition):
                self.lines = exec_chunk[:]

                for idx, ln in enumerate(self.lines):

                    stat = self.Prepline(idx)

                    if not stat:
                        return False
                
                n = self.vars.Get(for_var)
                n += for_step
                self.vars.Set(for_var, n)
                    
            self.lines = current_state
            del self.lines[a:b+1]
            self.vars.Delete(for_var)

            return True
        

    def EvalFunction(self, current_idx):
        def_line = [i.strip() for i in self.lines[current_idx].split("=") if i.strip()]

        if len(def_line) != 2:
            self.fail = "Invalid function declaration"
            return False
        
        fn_info = [i.strip() for i in def_line[1].split(":") if i.strip()]
        fn_name = fn_info[0]
        fn_args = fn_info[1:]

        a = current_idx + 1

        if self.lines[a] != "{":
            self.fail = "Couldn't find '{' to open function"
            return
        
        b = a+1
        ignore = 0
        found_close = False

        while b < len(self.lines):
            tar = self.lines[b].strip()

            if tar == "{":
                ignore += 1
            
            if tar == "}":
                if ignore:
                    ignore -= 1
                else:
                    found_close = True
                    break

            b += 1

        if not found_close:
            self.fail = "Couldn't find '}' to close function"
            return False
        
        fn_chunk = self.lines[a:b+1]

        if not fn_chunk[-2].startswith("RTN"):
            self.fail = "Function must be closed with RTN statement"
            return False
        
        self.custom_funcs.define(fn_name, fn_chunk[1:-1], fn_args)
        del self.lines[a:b+1]

        return True
    

    def ExtractFunction(self, parts):
        tar_info = self.custom_funcs.Get(parts[0])
        tar_name = tar_info.name
        tar_args = tar_info.args
        tar_argc = tar_info.argc
        tar_chunk = tar_info.chunk

        args = parts[1:]
        if len(args) != tar_argc:
            self.fail = f"{tar_name} takes {tar_argc} args: Found {len(args)}"
            return False
        
        current_state = self.lines
        current_vars = self.vars.vars

        self.lines = tar_chunk[:]
        self.vars.vars = {}

        for i in range(tar_argc):
            try:
                new_val = float(args[i])
            except:
                if args[i] in current_vars.keys():
                    new_val = float(current_vars[args[i]])
                else:
                    self.fail = f"Unrecognised var: {args[i]}"
                    return False
            
            self.vars.Set(tar_args[i], new_val)

        idx = 0
        while idx < len(self.lines):
            ln = self.lines[idx]

            if ln.startswith("RTN"):
                val = self.ExtractRTN(ln)

                if type(val) == bool and not val:
                    return False
                
                self.lines = current_state[:]
                self.vars.vars = current_vars

                return val

            else:
                if "FNC" in ln:
                    self.fail = "Cannot define function inside function"
                    return False
                
                if not self.Prepline(idx):
                    return False
            
            idx += 1

    
    def ExtractRTN(self, line):
        parts = [i.strip() for i in line.split("=")]
        
        if len(parts) != 2:
            self.fail = f"Invalid return expression: {line}"
            return False
        
        try:
            val = float(parts[1])
        except:

            if self.vars.has_var(parts[1]):
                val = float(self.vars.Get(parts[1]))

            else:
                self.fail = f"Unrecognised var: {parts[1]}"
                return False
        
        return val