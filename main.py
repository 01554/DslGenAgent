import src.dslautogen as dslautogen
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--user_request", type=str, default="テキストを受け取り（上限10000文字）、そのテキストから俳句を生成する")
    parser.add_argument("--output_path", type=str, default="dsl.yml")
    args = parser.parse_args()
    
    dslautogen.main(args.user_request, args.output_path)
