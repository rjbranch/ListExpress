from django.http import Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404, get_list_or_404, render
from .models import ItemList, Item, ItemComparison
from django.contrib.auth.decorators import login_required
import random

def index(request):
    context = {}

    #Gets the User information
    user = None
    if request.user.is_authenticated():
        user = request.user

    #Gets information on existing ItemLists
    itemlists = ItemList.objects.all()
    context['itemlists'] = itemlists

    #If the user is logged in, we include their lists separately
    user_itemlists = []
    if user:
        user_itemlists = user.member.itemlist_set.all()
    context['user_itemlists'] = user_itemlists
    context['user'] = user

    return render(request, 'listexpress/index.html', context)

def listdetail(request, itemlist_id):
    context = {}

    #Gets the User information
    user = None
    if request.user.is_authenticated():
        user = request.user

    #Gets the ItemList and Item information
    itemlist = get_object_or_404(ItemList, pk=itemlist_id)
    items = itemlist.item_set.all()
    context['itemlist'] = itemlist
    context['items'] = items
    if itemlist.fully_defined:
        comparisons = itemlist.itemcomparison_set.all()
        context['comparisons'] = comparisons

    #Determines if the ItemList was created by the User
    userOwnsList = False
    if user:
        if user == itemlist.member.user:
            userOwnsList = True
    context['userOwnsList'] = userOwnsList

    return render(request, 'listexpress/listdetail.html', context)

def comparisonvote(request, itemlist_id, votedComparison_id=None, vote=None):
    context = {}

    #Votes on the old content, if applicable
    if not (votedComparison_id is None):
        if not (vote is None):
            votedComparison = get_object_or_404(ItemComparison, pk=votedComparison_id)

            #If the user voted that item1 > item2
            if vote == '1':
                votedComparison.true_votes += 1
                votedComparison.save()

            #If the user voted that item2 > item1
            elif vote == '2':
                votedComparison.false_votes += 1
                votedComparison.save()

            #If vote is not '1' or '2'
            else:
                print(vote)
                return HttpResponseForbidden('<h1>vote must be a string equal to either \'1\' or \'2\'</h1>')
        else:
            return HttpResponseForbidden('<h1>A comparison_id was provided, but vote=None</h1>')

    #Generates the new content to be voted on
    #Gets the ItemList, ItemComparison and Item information
    itemlist = get_object_or_404(ItemList, pk=itemlist_id)
    comparisonIndex = random.randrange(itemlist.num_comparisons)
    itemcomparison = itemlist.itemcomparison_set.all()[comparisonIndex]
    items = itemlist.item_set.all()
    item1 = items[itemcomparison.item1_index]
    item2 = items[itemcomparison.item2_index]
    context['itemlist'] = itemlist
    context['itemcomparison'] = itemcomparison
    context['item1'] = item1
    context['item2'] = item2

    return render(request, 'listexpress/comparisonvote.html', context)

@login_required
def buildcomparisons(request, itemlist_id):
    context = {}

    #Gets the ItemList information
    itemlist = get_object_or_404(ItemList, pk=itemlist_id)

    #Ensure that the user calling this view is the owner of the list
    user = request.user
    creator = itemlist.member.user
    if user != creator:
        return HttpResponseForbidden('<h1>You are not authorized to build comparisons for a list which you did not create</h1>')
    else:
        itemlist = get_object_or_404(ItemList, pk=itemlist_id)
        items = itemlist.item_set.all()
        numItems = items.count()
        numComparisons = itemlist.itemcomparison_set.count()
        itemlist.fully_defined = ((numComparisons) == ((numItems * numItems - numItems) / 2))
        print("FULLY DEFINED:" + str(itemlist.fully_defined))

        #If the comparisons have not been built yet or were built incorrectly
        if not itemlist.fully_defined:
            for i in range(numItems - 1):
                for j in range(i + 1, numItems):
                    itemlist.itemcomparison_set.create(item1_index=i,
                                                       item2_index=j,
                                                       comparison_name=(items[i].item_name +
                                                                        " vs. " +
                                                                        items[j].item_name))
            itemlist.num_items = numItems
            itemlist.fully_defined = True
            itemlist.save()
            itemcomparisons = itemlist.itemcomparison_set.all()
            context['itemlist'] = itemlist
            context['itemcomparisons'] = itemcomparisons
            return render(request, 'listexpress/buildcomparisons.html', context)

        #If the comparisons have already been built
        else:
            return HttpResponseForbidden('<h1>You are not authorized to rebuild comparisons for this list</h1>')