from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from conversation.forms import ConversationMessageForm
from conversation.models import Conversation
from product.models import Product


# Create your views here.
@login_required
def new_conversation(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk)
    if product.created_by == request.user:
        return redirect('dashboard:index')

    conversations = Conversation.objects.filter(product=product).filter(members__in=[request.user.id])

    if conversations:
        return redirect('conversation:detail', pk=conversations.first().id)

    if request.method == "POST":
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation = Conversation.objects.create(product=product)
            conversation.members.add(request.user)
            conversation.members.add(Product.created_by)
            conversation.save()

            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            return redirect('product:detail', pk=product_pk)

    else:
        form = ConversationMessageForm()
    return render(request, 'conversation/new.html', {
        'form': form,
    })


@login_required
def inbox(request):
    conversations = Conversation.objects.filter(members__in=[request.user.id])
    return render(request, 'conversation/inbox.html', {
        'conversations': conversations
    })


@login_required
def detail(request, pk):
    conversation = Conversation.objects.filter(members__in=[request.user.id].get(pk=pk))

    if request.method == "POST":
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()
            conversation.save()
            return redirect('conversation:detail', pk=pk)
    else:
        form = ConversationMessageForm()

    return render(request, 'conversation/detail.html', {
        'conversation': conversation,
        'form':form,
    })
