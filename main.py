import src.dslautogen as dslautogen
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--user_request", type=str,
                      help="直接リクエストを指定する場合に使用")
    group.add_argument("--request_file", type=str,
                      help="優先:リクエストを記載したファイルのパス")
    parser.add_argument("--output_path", type=str, default="dsl.yml")
    args = parser.parse_args()
    
    if args.request_file:
        with open(args.request_file, 'r', encoding='utf-8') as f:
            user_request = f.read().strip()
    else:
        user_request = args.user_request
    
    dslautogen.main(user_request, args.output_path)
