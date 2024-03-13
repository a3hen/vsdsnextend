import argparse
import controller


# ----以下是一级命令行----
# python3 main.py
# python3 main.py create(c)
# # 创建密码



class argparse_operator:
    def __init__(self):
        self.parser = argparse.ArgumentParser(prog='vsdsnextend')
        self.setup_parse()

    def setup_parse(self):
        sub_parser = self.parser.add_subparsers()

        self.parser.add_argument('-v',
                                 '--version',
                                 dest='version',
                                 help='Show current version',
                                 action='store_true')

        parser_kernel = sub_parser.add_parser("kernel",aliases=['k'],help='create passphrase')


        self.parser.set_defaults(func=self.main_usage)
        parser_kernel.set_defaults(func=self.kernel_operation)


    def perform_all_tests(self,args):
        self.parser.print_help()

    def main_usage(self,args):
        if args.version:
            print(f'Version: v1.0.0')
        else:
            print(f"python3 main.py")

    def kernel_operation(self,args):
        print("替换内核")
        obj = controller.vsdsinstaller_k.replacement_installation.ReplacementInstallation()
        obj.change_kernel()

    def parser_init(self):
        args = self.parser.parse_args()
        args.func(args)


if __name__ == "__main__":
    cmd = argparse_operator()
    cmd.parser_init()

