import gdb

class TinyAllocDumpCmd(gdb.Command):
    """Prints the ListNode from our example in a nice format!"""

    def __init__(self):
        super(TinyAllocDumpCmd, self).__init__(
            "dump_tiny_alloc", gdb.COMMAND_USER
        )

    def dump_block(self, name):
        heap = gdb.parse_and_eval("heap")
        currentBlock = heap[name]

        result = f"\n{name}: {currentBlock}\n"
        char = gdb.lookup_type('char')
        while currentBlock != 0:
            addr = currentBlock['addr']
            result += f"{currentBlock} = {{\n"
            result += f"\taddr = {addr},\n"
            result += f"\tnext = {currentBlock['next']},\n" 
            result += f"\tsize = {currentBlock['size']},\n"
            if addr != 0:
                s = str(addr.cast(char.pointer()))
                s = s.replace(hex(addr), "")
                result += f"\tcontent ={s}\n"
            result += "}\n"
            currentBlock = currentBlock["next"]

        return result

    def dump(self):
        """Walk through the UuidListNode list.

        We will simply follow the 'next' pointers until we encounter NULL
        """
        heap = gdb.parse_and_eval("heap")
        top = heap["top"]
        limit = gdb.parse_and_eval("heap_limit")
        blocks = gdb.parse_and_eval("heap_max_blocks")

        result = f"Heap start: \t{heap}\n"
        result += f"Heap top: \t{top}\n"
        result += f"Heap limit: \t{limit}\n"
        result += "Heap blocks: \t%d" % blocks

        result += self.dump_block("free")
        result += self.dump_block("used")
        result += self.dump_block("fresh")

        return result

    def complete(self, text, word):
        # We expect the argument passed to be a symbol so fallback to the
        # internal tab-completion handler for symbols
        return gdb.COMPLETE_SYMBOL

    def invoke(self, args, from_tty):
        # We can pass args here and use Python CLI utilities like argparse
        # to do argument parsing
        print(self.dump())

TinyAllocDumpCmd()

class AllocBreakpoint(gdb.Breakpoint):
    def __init__(self):
        gdb.Breakpoint.__init__(self, "ta_alloc")

    def stop(self):
        frame = gdb.selected_frame() # Use the current frame
        # Find all the arguments in the current block
        args = [arg for arg in frame.block() if arg.is_argument]

        size = None
        for arg in args:
            size = str(arg.value(frame))
            break

        AllocBreakpointFinish(frame, size)

AllocBreakpoint()

class AllocBreakpointFinish(gdb.FinishBreakpoint):
    def __init__(self, frame, size) -> None:
        self.size = size
        gdb.FinishBreakpoint.__init__(self, frame)

    def stop(self):
        print(f"{self.return_value} = ta_alloc({self.size})")