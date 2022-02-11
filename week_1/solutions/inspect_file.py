## part of the solution set for DAPOM practical week 1
# author: Nick Szirbik
# date: 6 February 2022


def show_file_content(file_name):
    file = open("storage.txt")
    print('The text file "storage" is now open\n')
    print('---------file content---------')
    print(file.read())
    print('----------end of file content-------')
    file.close()
    print('The text file "storage" is now close')
