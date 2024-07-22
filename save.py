from story import serifs


class Save:
    def __init__(self, save) -> None:
        # if "chapter" not in save:
        #     save["chapter"] = 0
        # if "branch" not in save:
        #     save["branch"] = "first"
        # if "text_num" not in save:
        #     save["text_num"] = 0
        # if "name" not in save:
        #     save["name"] = "もこた"
        # if "credits" not in save:
        #     save["credits"] = [0, 0, 0]

        self.save_data = save

    def current_text(self, max_letter_num: int):
        element_list = serifs[self["chapter"]][self["branch"]]

        # もし今いるブランチの長さを越えているならデータ破損
        if len(element_list) <= self["text_num"]:
            return "Error"

        current_text = element_list[self["text_num"]]

        num = 1
        while type(current_text) == list:
            current_text = element_list[self["text_num"] - num]
            num += 1

        if type(current_text) != str:
            current_text = "ERROR"
        # print(type(current_text))

        if len(current_text) > max_letter_num:
            current_text = current_text[:max_letter_num] + "..."

        return current_text.replace(";", "  ").format(name=self["name"])

    def __setitem__(self, index, value):
        self.save_data[index] = value

    def __getitem__(self, index):
        return self.save_data[index]
