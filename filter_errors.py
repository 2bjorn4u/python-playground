with open("app.log", "r") as src, \
    open("errors.log", "w+") as dst:

    for line in src:
        if "ERROR" in line:
            dst.write(line)
    dst.seek(0)
    for line in dst:
        print(line, end="")


# with open("app.log", "r") as file:
#     with open("errors.log", "w+") as errors:
#         contents = file.readlines()
#         error_count = 0
#         line_count = 0

#         for line in contents:
#             line_count += 1
#             print(f"Line {line_count}")
#             print(line)
#             if "ERROR" in line:
#                 error_count += 1
#                 errors.write(line.strip() + "\n")

#         print(f"Error count: {error_count}")
#         errors.seek(0)
#         for line in errors.readlines():
#             print(line)