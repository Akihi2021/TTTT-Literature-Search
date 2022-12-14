from context import openAlex


def get_papers(author_id):
    works = []

    try:
        works = openAlex.get_list_of_works(
            filters={
            'author.id': 'https://openalex.org/A' + author_id
            },
            per_page=200
        )
    finally:
        return works


def get_id_and_title_and_type_of_papers(author_id):
    data = []

    try:
        works = get_papers(author_id)
        for work in works:
            for result in work.get('results'):
                data.append({
                    'id': result.get('id'),
                    'title': result.get('title'),
                    'type': result.get('type')
                })

                if len(data) > 200:
                    return data
    finally:
        return data


def get_related_authors(author_id):
    data = []
    seen = set()
    flag = False

    try:
        works = get_papers(author_id)
        for work in works:
            if flag:
                break

            for result in work.get('results'):
                if flag:
                    break

                authorships = result.get("authorships")
                for item in authorships:
                    author = item.get("author")
                    id = author.get("id").split('/')[-1][1:]
                    name = author.get("display_name")
                    if id != author_id and name not in seen:
                        data.append({
                            "name": name,
                            "id": id}
                        )
                        seen.add(name)

                    if len(data) > 100:
                        flag = True
                        break

    finally:
        return data


if __name__ == "__main__":
    # print(len(get_related_authors("2175547780")))
    print(len([_ for _ in get_id_and_title_and_type_of_papers("2175547780")]))
