from context import openAlex


def get_papers(author_id):
    works = openAlex.get_list_of_works(filters={
        'author.id': 'https://openalex.org/A' + author_id
    })

    return works

def get_title_and_type_of_papers(author_id):
    works = get_papers(author_id)
    data = []
    for work in works:
        for result in work.get('results'):
            data.append({
                'title': result.get('title'),
                'type': result.get('type')
            })

    return data


def get_related_authors(author_id):
    works = get_papers(author_id)

    data = []
    for work in works:
        for result in work.get('results'):
            authorships = result.get("authorships")
            for item in authorships:
                author = item.get("author")
                id = author.get("id").split('/')[-1][1:]
                name = author.get("display_name")
                if id != author_id:
                    data.append(name)

    return data


if __name__ == "__main__":
    print(get_related_authors("2208157607"))
