import random
import string


def create_file(name_f, dir_path, size):
    if not size.isdigit():
        if size.endswith('KB'):
            s1 = size.split('KB')
            size1 = int(s1[0]) * 1024
            token = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) 
                            for _ in range(size1))
        elif size.endswith('MB'):
            s1 = size.split('MB')
            size1 = int(s1[0]) * 1048567
            token = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) 
                            for _ in range(size1))
        elif size.endswith('GB'):
            s1 = size.split('GB')
            size1 = int(s1[0]) * 1073741824
            token = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) 
                            for _ in range(size1))
    else:
        token = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) 
                        for _ in range(int(size)))
    with open(dir_path + name_f, "w") as file:  # По-хорошшему, здесь нужно использовать os.path.join(dir_path, name_f)
        file.write(token)
        

create_file("/test1.txt", "E:", '10KB')
create_file("/test2.txt", "E:", '1024')
create_file("/test11.txt", "E:", '2MB')
create_file("/test21.txt", "E:", '1B')
