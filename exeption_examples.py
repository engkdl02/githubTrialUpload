# from random import sample
#
# from pydantic.experimental.pipeline import transform
#
#
# def prepare_user(raw_user_data):
#     extracted_user_data = extract_user_data(raw_user_data)
#     fixed_user_data = fix_user_data(extracted_user_data)
#     transformed_user_data = transform_user_data(fixed_user_data)
#     return transformed_user_data
#
# def insert_user_into_db(user_data):
#     try:
#         if not check_if_user_in_database(user_data):
#             inser_into_db(user_data)
#     except Exception as e:
#         pass
#
#
# sample_dict = {"a": 1}
#
# print(sample_dict)
# print(sample_dict["a"])
#
# try:
#     # print(sample_dict["b"])
#     1/0
# except ZeroDivisionError:
#     print("wheve encountered a key error")
#
#
# # except Exception as e:
# #     print("oh no, you encountered an exception or error: ", str(e))
#
# print("it didn't work until here so you need exception handling")