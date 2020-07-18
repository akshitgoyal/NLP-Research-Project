

def run(lst):
    # lst = [('Vishnu', 'Varma'), ('Akshit', 'Goyal')]
    lst_len = len(lst)
    n_lst = lst_len // 100
    n_lst_count = 0
    gender_lst = []
    ethnicity_lst = []
    while n_lst >= 0:
        if n_lst == 0:
            size = lst_len % 100
        else:
            size = 100
        if size != 0:
            gender_lst.append({"personalNames": []})
            ethnicity_lst.append({"personalNames": []})
            for i in range(n_lst_count*100, n_lst_count*100 + size):
                # index = i + n_lst_count*100
                name = lst[i][0] + ' ' + lst[i][1]
                gender_lst[n_lst_count]["personalNames"].append({"id": str(i), "name": name})
                ethnicity_lst[n_lst_count]["personalNames"].append({"id": str(i), "firstName": lst[i][0], "lastName": lst[i][1]})
            n_lst_count += 1
        n_lst -= 1

    #
    # print(len(gender_lst))
    # print("========================")
    # print(len(ethnicity_lst))

    return gender_lst
