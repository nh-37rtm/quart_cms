
import asyncio
import sys

import subprocess


class AsyncPopenWrapper():
        
    async def popen(self, cmd: str, stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE, stderr=sys.stderr, **kwds) \
        -> tuple[asyncio.queues.Queue[str], asyncio.queues.Queue[str]]:
        
        in_data:asyncio.queues.Queue[str] = asyncio.queues.Queue()
        out_data:asyncio.queues.Queue[str] = asyncio.queues.Queue()

        descriptor = subprocess.Popen(cmd, shell= True, bufsize=0, stdin= stdin, stdout= stdout, stderr=sys.stderr)
        
        async def inpipe():
            while True:
                await asyncio.sleep(0)
                item = await in_data.get()
                
                if item is None:
                    break
                    
                descriptor.stdin.write(f"{item}\n".encode())
                descriptor.stdin.flush()

            descriptor.stdin.close()
            
        async def outpipe():
            
            while True:
                await asyncio.sleep(0.1)
                result = descriptor.stdout.readline().strip()
                if not result:
                    break
                await out_data.put(result)
                
            await out_data.put(None)
            descriptor.stdout.close()
        
            
            
        tasklist = [ inpipe(), outpipe() ]

        return (tasklist, in_data, out_data)
    