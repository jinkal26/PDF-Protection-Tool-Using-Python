import argparse
import os
import sys

try:
    from PyPDF2 import PdfReader, PdfWriter
except ImportError:
    print("PyPDF2 is not installed. Install it with: pip install PyPDF2")
    sys.exit(1)


def parse_args():
    parser = argparse.ArgumentParser(description="Encrypt a PDF (set a user password and optional owner password).")
    parser.add_argument("input_pdf", help="Path to the input PDF file")
    parser.add_argument("-o", "--output", help="Output path for encrypted PDF. Defaults to <input>_protected.pdf")
    parser.add_argument("-p", "--password", required=True, help="User password required to open the encrypted PDF")
    parser.add_argument("--owner-password", help="Owner password (optional). If omitted, owner password == user password")
    parser.add_argument("--input-password", help="Password to unlock the input PDF if it is already encrypted")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite output file if it exists")
    parser.add_argument("--no-metadata", action="store_true", help="Do not copy metadata from source PDF")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    return parser.parse_args()


def main():
    args = parse_args()

    input_path = args.input_pdf
    if not os.path.exists(input_path):
        print(f"Error: input file not found: {input_path}")
        sys.exit(2)

    if not args.output:
        base, ext = os.path.splitext(input_path)
        ext = ext or ".pdf"
        args.output = f"{base}_protected{ext}"

    if os.path.exists(args.output) and not args.overwrite:
        print(f"Error: output file '{args.output}' already exists. Use --overwrite to replace it.")
        sys.exit(3)

    try:
        with open(input_path, "rb") as inf:
            try:
                reader = PdfReader(inf)
            except Exception as e:
                print(f"Error: failed to read input PDF: {e}")
                sys.exit(4)

            # If the input PDF is encrypted, try to decrypt with provided input password
            if getattr(reader, "is_encrypted", False):
                if not args.input_password:
                    print("Error: input PDF is encrypted. Provide --input-password to open it.")
                    sys.exit(5)
                try:
                    dec = reader.decrypt(args.input_password)
                    # decrypt() may return 0/1, True/False, or raise depending on PyPDF2 version
                    if dec == 0 or dec is False:
                        print("Error: failed to decrypt input PDF with the provided input password.")
                        sys.exit(6)
                except Exception as e:
                    print(f"Error: failed to decrypt input PDF: {e}")
                    sys.exit(6)

            writer = PdfWriter()

            # Copy pages
            try:
                for page in reader.pages:
                    writer.add_page(page)
            except Exception as e:
                print(f"Error while copying pages: {e}")
                sys.exit(7)

            # Optionally copy metadata
            if not args.no_metadata:
                try:
                    if hasattr(reader, "metadata") and reader.metadata:
                        writer.add_metadata(reader.metadata)
                except Exception:
                    if args.verbose:
                        print("Warning: failed to copy metadata (continuing).")

            owner_pwd = args.owner_password if args.owner_password is not None else args.password

            # Apply encryption. Different PyPDF2/pypdf versions have slightly different signatures,
            # so try a couple of ways to call encrypt() and fail gracefully.
            try:
                # common signature: encrypt(user_pwd, owner_pwd)
                writer.encrypt(args.password, owner_pwd)
            except TypeError:
                try:
                    # some versions accept named args
                    writer.encrypt(user_pwd=args.password, owner_pwd=owner_pwd)
                except Exception as e:
                    print(f"Error: failed to encrypt PDF: {e}")
                    sys.exit(8)

            # Write the encrypted PDF to disk
            try:
                with open(args.output, "wb") as outf:
                    writer.write(outf)
            except Exception as e:
                print(f"Error while writing output PDF: {e}")
                sys.exit(9)

    except FileNotFoundError:
        print(f"Error: file not found: {input_path}")
        sys.exit(2)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(99)

    print(f"Success: encrypted PDF saved to: {args.output}")


if __name__ == "__main__":
    main()
