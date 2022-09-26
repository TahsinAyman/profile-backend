import json

from app import get_comments

pages = {
    "1": [
        {
            "id": 1,
            "name": "John",
            "comment": "Nice Website Bro."
        },
        {
            "id": 2,
            "name": "Mosh",
            "comment": "Nice Website. I want that"
        },
        {
            "id": 3,
            "name": "TahsinAyman",
            "comment": "Please Enjoy This Website.\nIt is a small profile for myself.\nI can also make your profiles.\nPlease Contact at mail4tahsin@gmail.com"
        },
        {
            "id": 4,
            "name": "John",
            "comment": "Nice Website Bro."
        },
        {
            "id": 5,
            "name": "John",
            "comment": "Nice Website Bro."
        }
    ],
    "2": [
        {
            "id": 6,
            "name": "John",
            "comment": "Nice Website Bro."
        },
        {
            "id": 7,
            "name": "John",
            "comment": "Nice Website Bro."
        },
        {
            "id": 8,
            "name": "John",
            "comment": "Nice Website Bro."
        },
        {
            "id": 9,
            "name": "John",
            "comment": "Nice Website Bro."
        },
        {
            "id": 10,
            "name": "John",
            "comment": "Nice Website Bro."
        }
    ],
    "3": [
        {
            "id": 11,
            "name": "John",
            "comment": "Nice Website Bro."
        },
        {
            "id": 12,
            "name": "John",
            "comment": "Nice Website Bro."
        },
        {
            "id": 13,
            "name": "John",
            "comment": "Nice Website Bro."
        },
        {
            "id": 14,
            "name": "John",
            "comment": "Nice Website Bro."
        }
    ]
}
# for i in range(1, len(pages) + 1):
#     for y in pages[i - 1]:
#         y["page"] = i


print(json.dumps(obj=get_comments(), indent=4))
