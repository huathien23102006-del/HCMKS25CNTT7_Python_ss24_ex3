"""
    (1) Phân tích thiết kế (Code Review & Architecture)
    1. Vì sao point_value_vnd là Class Attribute?

    point_value_vnd là quy định chung của toàn hệ thống:

    1 điểm = 1000 VNĐ

    Nó không thuộc về riêng một khách hàng nào.

    Nếu đặt trong __init__:

    self.point_value_vnd = 1000

    thì mỗi object sẽ có một bản sao riêng:

    card1
    └── point_value_vnd = 1000

    card2
    └── point_value_vnd = 1000

    Khi chạy chức năng 5:

    update_point_value(2000)

    chỉ đổi được 1 thẻ.

    Các thẻ khác vẫn:

    card1 = 2000
    card2 = 1000
    card3 = 1000

    => Sai yêu cầu hệ thống.

    Dùng:

    Class Attribute

    thì tất cả object dùng chung:

    MemberCard
    └── point_value_vnd = 2000

    card1
    card2
    card3
        |
        dùng chung
    2. Vì sao is_valid_card_id dùng @staticmethod?

    Hàm này chỉ kiểm tra:

    RC01
    RC99

    Nó không cần:

    điểm
    tên khách
    dữ liệu của object

    Nên không cần tạo:

    card = MemberCard(...)

    mới kiểm tra được.

    Có thể gọi trực tiếp:

    MemberCard.is_valid_card_id("RC01")
    3. Encapsulation với __points giải quyết gì?

    Nếu để:

    card.points = 100000

    thì khách hàng/nhân viên có thể gian lận.

    Dùng:

    self.__points

    thì điểm chỉ thay đổi qua:

    earn_points()
    redeem_points()

    => Kiểm soát toàn bộ nghiệp vụ cộng/trừ điểm.
"""

class MemberCard:


    # Class Attribute
    point_value_vnd = 1000



    def __init__(self, card_id, name):

        self.card_id = card_id
        self.name = name

        # private attribute
        self.__points = 0
        self.__tier = "Standard"



    # Getter điểm

    @property
    def points(self):

        return self.__points



    # Getter hạng

    @property
    def tier(self):

        return self.__tier



    # tích điểm

    def earn_points(self, bill_amount):

        earned = bill_amount // 10000

        self.__points += earned


        if self.__points >= 100:

            if self.__tier != "VIP":

                self.__tier = "VIP"

                print(
                    "Chúc mừng! Khách hàng đã được nâng hạng lên VIP."
                )


        return earned



    # đổi điểm

    def redeem_points(self, points_to_use):

        if points_to_use <= 0:

            print("Số điểm sử dụng không hợp lệ!")

            return False



        if points_to_use > self.__points:

            print(
                "Không thể đổi điểm!"
            )

            print(
                "Số điểm muốn sử dụng vượt quá số điểm hiện có."
            )

            return False



        self.__points -= points_to_use


        discount = (
            points_to_use *
            MemberCard.point_value_vnd
        )


        print(
            f"Đã trừ {points_to_use} điểm."
        )

        print(
            f"Khách hàng được giảm giá {discount:,} VNĐ vào hóa đơn!"
        )


        return True



    # kiểm tra mã thẻ

    @staticmethod
    def is_valid_card_id(card_id):

        if len(card_id) != 4:

            return False


        if not card_id.startswith("RC"):

            return False


        if not card_id[2:].isdigit():

            return False


        return True



    # cập nhật tỷ giá

    @classmethod
    def update_point_value(cls,new_value):

        if new_value > 0:

            cls.point_value_vnd = new_value

            print(
                "Cập nhật tỷ giá thành công!"
            )

        else:

            print(
                "Tỷ giá không hợp lệ!"
            )





# ===============================
# MAIN PROGRAM
# ===============================


cards_database = []



while True:


    print("""
===== HỆ THỐNG THẺ THÀNH VIÊN RIKKEI COFFEE =====

1. Xem danh sách thẻ thành viên
2. Đăng ký thẻ mới
3. Khách mua hàng (Tích điểm)
4. Khách dùng điểm (Đổi ưu đãi)
5. Cập nhật tỷ giá quy đổi điểm
6. Thoát
""")


    choice = input(
        "Chọn chức năng: "
    )



    # Xem danh sách

    if choice == "1":


        if len(cards_database) == 0:

            print("Chưa có thẻ nào!")

        else:

            for index,card in enumerate(cards_database,1):

                print(
                    f"{index}. "
                    f"Mã: {card.card_id} | "
                    f"Tên: {card.name} | "
                    f"Điểm: {card.points} | "
                    f"Hạng: {card.tier}"
                )




    # Đăng ký

    elif choice == "2":


        card_id = input(
            "Nhập mã thẻ: "
        )


        if not MemberCard.is_valid_card_id(card_id):

            print(
                "Mã thẻ không hợp lệ!"
            )

            continue



        exists = False


        for card in cards_database:

            if card.card_id == card_id:

                exists = True



        if exists:

            print(
                "Mã thẻ đã tồn tại!"
            )

            continue



        name = input(
            "Nhập tên khách hàng: "
        )


        card = MemberCard(
            card_id,
            name.title()
        )


        cards_database.append(card)


        print(
            "Đăng ký thẻ thành công!"
        )





    # mua hàng

    elif choice == "3":


        card_id = input(
            "Nhập mã thẻ: "
        )


        bill = int(
            input("Nhập tổng tiền hóa đơn: ")
        )


        for card in cards_database:


            if card.card_id == card_id:


                point = card.earn_points(bill)


                print(
                    f"Số điểm tích: {point}"
                )


                print(
                    f"Tổng điểm: {card.points}"
                )


                print(
                    f"Hạng: {card.tier}"
                )





    # đổi điểm

    elif choice == "4":


        card_id = input(
            "Nhập mã thẻ: "
        )


        use = int(
            input("Nhập số điểm muốn dùng: ")
        )



        for card in cards_database:


            if card.card_id == card_id:


                card.redeem_points(use)


                print(
                    f"Số điểm còn lại: {card.points}"
                )

                print(
                    f"Hạng: {card.tier}"
                )





    # đổi tỷ giá

    elif choice == "5":


        print(
            f"Tỷ giá hiện tại: {MemberCard.point_value_vnd}"
        )


        value = int(
            input("Nhập tỷ giá mới: ")
        )


        MemberCard.update_point_value(value)


        print(
            f"Tỷ giá mới: {MemberCard.point_value_vnd}"
        )





    elif choice == "6":


        print(
            "Cảm ơn bạn đã sử dụng hệ thống!"
        )

        break



    else:

        print(
            "Lựa chọn không hợp lệ!"
        )