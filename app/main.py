import sys
import os
import zlib
from hashlib import sha1


def main():

    command = sys.argv[1]
    if command == "init":
        os.mkdir(".git")
        os.mkdir(".git/objects")
        os.mkdir(".git/refs")
        with open(".git/HEAD", "w") as f:
            f.write("ref: refs/heads/master\n")
        print("Initialized git directory")
    elif command == "cat-file":
        if not sys.argv[2] == "-p":
            raise RuntimeError(f"Unexpected flag #{sys.argv[2]}")
        dname, fname = sys.argv[3][:2], sys.argv[3][2:]
        with open(os.path.join(".git/objects", dname, fname), "rb") as f:
            _, output = zlib.decompress(f.read()).split(b"\x00")
        sys.stdout.buffer.write(output)
    elif command == "hash-object":
        if not sys.argv[2] == "-w":
            raise RuntimeError(f"Unexpected flag #{sys.argv[2]}")

        with open(sys.argv[3], "rb") as f:
            contents = f.read()

        header = f"blob {len(contents)}\x00".encode("utf-8")
        hash = sha1(header + contents).hexdigest()
        print(hash)
        dname, fname = hash[:2], hash[2:]
        dname = os.path.join(".git/objects", dname)
        os.mkdir(dname)
        with open(os.path.join(dname, fname), "wb") as f:
            f.write(zlib.compress(header + contents))

    elif command == "ls-tree":
        if not sys.argv[2] == "--name-only":
            raise RuntimeError(f"Unexpected flag #{sys.argv[2]}")
        dname, fname = sys.argv[3][:2], sys.argv[3][2:]
        with open(os.path.join(".git/objects", dname, fname), "rb") as f:
            _, treedata = zlib.decompress(f.read()).split(b"\x00", 1)
            res = []
            while treedata:
                # we don't need the mode
                _, treedata = treedata.split(b" ", 1)
                entry, treedata = treedata.split(b"\x00", 1)
                res.append(entry)
                treedata = treedata[20:]
            print("\n".join(res))

    elif command == "write-tree":
        res = b""
        entries = os.scandir()
        for entry in entries:
            mode = f"{entry.stat().st_mode:o}"

        raise RuntimeError("write-tree not implemented yet")

    else:
        raise RuntimeError(f"Unknown command #{command}")


if __name__ == "__main__":
    main()
