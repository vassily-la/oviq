from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def pg_records(request, list, num):
    paginator = Paginator(list, num)

    # Get the page number from the query string
    # If the page aparam is available,
    # get() will return an empty string ""
    page = request.GET.get('page')

    try:
        page_object = paginator.page(page)
    except PageNotAnInteger:
        page_object = paginator.page(1)
    except EmptyPage:
        page_object = paginator.page(paginator.num_pages)
    return page_object
