from typing import List


class Crypt:
    @staticmethod
    def Encrypt(s: str, n: int, e: int) -> str:
        arr: List[int] = [ord(s[i]) for i in range(len(s))]
        while len(arr) % 4 != 0:
            arr.append(0)

        out = ""
        for i in range(len(arr) - 1):
            if i % 4 == 0:
                x: int = ((arr[i] * 256 + arr[i + 1]) * 256 + arr[i + 2]) * 256 + arr[
                    i + 3
                ]
                encryptedBlock: int = pow(x, e, n)
                # encryptedBlock = x
                out += f"{encryptedBlock} "
        return out


if __name__ == "__main__":
    import sys

    toEncrypt: str = input()
    n: int = int(sys.argv[1])
    e: int = int(sys.argv[2])
    print(Crypt.Encrypt(toEncrypt, n, e))
