def create_file(content, file_name, file_extension, folder=None):
    if folder:
        if file_extension:
            file_path = "{}/{}.{}".format(folder, file_name, file_extension)
        else:
            file_path = "{}/{}".format(folder, file_name)
    else:
        if file_extension:
            file_path = "{}.{}".format(file_name, file_extension)
        else:
            file_path = "{}".format(file_name)
    # write to file
    with open(file_path, "wb") as f:
        f.write(content.encode('utf8'))
    return file_path
