import argparse
import sys 

class Cache:
    def __init__(self, size_limit = 0):
        self.cache = {}
        self.size_limit = size_limit # in bytes

    def get(self, key):
        return self.cache.get(key, "")
    
    def set(self, key, value, ttl):
        if self._get_cache_size() > self.size_limit:
            return "" # not allowing user to save
        
        self.cache[key] = value
        return value
    
    def delete(self, key):
        if self.cache.get(key, None):
            del self.cache[key]
            return key
        return ""
    
    def _get_cache_size(self):
        return sys.getsizeof(self.cache)

    def execute(self, command):
        parts = command.split()
        if len(parts) < 2:
            return "Operation is not allowed"
        
        operation = parts[0].lower()

        operation_map = {
            "get": self.get,
            "set": self.set,
            "del": self.delete,
        }

        if operation not in operation_map:
            return "Operation is not allowed"

        if operation == "set":
            key = parts[1]
            value = parts[2]
            res = operation_map[operation](key, value)
        else:
            key = parts[1]
            res = operation_map[operation](key)

        return res


def main():
    # parse arguments
    # --size-limit -> initialize cache object based on that limit
    parser = argparse.ArgumentParser("Cache CLI Application")
    parser.add_argument("--size-limit", type=str, help="Size limit (MB) for the application (required)")

    args = parser.parse_args()

    if not args.size_limit:
        size_limit = input("Please specify the size limit for your cache (in MB, default 1GB): ")
        args.size_limit = float(size_limit) * 1000000 if size_limit else 1000000000

    cache_app = Cache(size_limit=args.size_limit)


    while True:
        command = input("> ")

        if command == "exit":
            break

        print(cache_app.execute(command))

if __name__ == "__main__":
    main()