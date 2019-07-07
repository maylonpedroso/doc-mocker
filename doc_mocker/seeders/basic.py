import inspect
import random

from doc_mocker import fonts as fonts_module
from doc_mocker.models import Page, Text, TextType

FONTS = [
    obj
    for name, obj in inspect.getmembers(fonts_module)
    if inspect.isclass(obj) and fonts_module.Font in obj.__bases__
]


class Seeder:
    def seed(self, page: Page):
        raise NotImplementedError()


class BasicSeeder(Seeder):
    TEXTS = [
        Text("Lorem Ipsum", TextType.TITLE),
        Text(
            """Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur,
        adipisci velit..."""
        ),
        Text(
            """Lorem ipsum dolor sit amet, consectetur adipiscing elit.Ut suscipit, neque non
        sollicitudin venenatis, libero lacus elementum elit, eu euismod quam orci vitae neque.
        Integer tristique tempor purus sit amet luctus. Maecenas ac ipsum eros. Aenean euismod
        risus justo, pretium maximus nisl dictum a. Sed ac mattis erat. Duis eu urna laoreet,
        placerat urna gravida, congue augue. Quisque eget sodales nunc. Quisque at egestas nibh.
        Nunc mauris felis, interdum id consectetur at, gravida vitae neque.Phasellus semper
        posuere lacus. Phasellus semper, sapien eget feugiat porta, erat libero fermentum erat,
        sed tincidunt erat justo ac orci. Nulla accumsan tellus ac accumsan commodo. Nam ac
        varius lorem, et auctor erat. Nulla at tristique dolor. Duis neque arcu, luctus eu nisi
        in, dapibus accumsan dui."""
        ),
        Text(
            """Mauris ultricies massa eu eleifend hendrerit. Sed risus nibh, convallis et rhoncus
        sed, feugiat luctus dolor. Etiam fringilla porttitor ornare. Etiam sed ligula risus. Vivamus
        at metus libero. Vestibulum vestibulum porta posuere. Nulla sem mauris, consequat sed metus
        a, vulputate fermentum ligula. Nullam non lacus id sem faucibus pellentesque. Suspendisse
        imperdiet diam ac elit malesuada blandit nec sed est. Sed ultrices neque sit amet mi
        vulputate efficitur."""
        ),
        Text("Donec et interdum diam. Nulla facilisi.", TextType.SUBTITLE),
        Text(
            """Donec et interdum diam. Nulla facilisi. Maecenas semper, massa eget mattis molestie,
        justo nunc tempor augue, nec imperdiet sem felis sit amet augue. Sed ornare velit et augue
        aliquet, sed dignissim sapien imperdiet. Integer luctus blandit nunc at bibendum.
        Vivamus nibh eros, semper a nisl sit amet, mattis mollis purus. Integer a accumsan est.
        Donec ut feugiat arcu. Nam sit amet tortor pulvinar, fermentum massa vitae, placerat mauris.
        In ac felis cursus orci consequat congue."""
        ),
        Text(
            """In tellus magna, posuere nec tempor sit amet, pretium et mi. Mauris dignissim
        dignissim tempus."""
        ),
        Text(
            """Pellentesque volutpat cursus elementum. Mauris lobortis non dui at ultrices. Duis
        turpis ante, malesuada sed aliquam vitae, egestas a tellus. Fusce dapibus nisi at nulla
        ultrices lobortis. Morbi condimentum felis in egestas egestas. Curabitur viverra nibh quis
        ligula fringilla auctor. Morbi in tempor erat. Integer id leo nec eros commodo auctor quis
        sit amet nulla. Etiam venenatis interdum euismod. Curabitur pharetra ligula ut sapien
        pharetra facilisis."""
        ),
        Text(
            """Mauris non mollis dolor, sed vulputate nisi. Nullam vitae volutpat mauris, ac molestie
        tortor. Maecenas cursus diam pellentesque justo molestie, et placerat nulla aliquam.Duis
        pharetra ligula vel vestibulum venenatis. Pellentesque habitant morbi tristique senectus et
        netus et malesuada fames ac turpis egestas. Vestibulum ac pellentesque ante, nec
        pellentesque tellus."""
        ),
        Text(
            """Mauris ultrices ut magna eu volutpat. Orci varius natoque penatibus et magnis dis
        parturient montes, nascetur ridiculus mus.  Donec enim turpis, vestibulum vel sollicitudin
        sollicitudin, viverra vel eros. Donec ut tempor arcu, a tincidunt augue."""
        ),
    ]

    BOOL_CHOICES = [True] + [False] * 9

    def seed(self, page: Page):
        font_class = random.choice(FONTS)
        font = random.choice([font_class(size) for size in range(9, 17)])
        while not page.is_full:
            text = random.choice(self.TEXTS)
            page.write(text, font)
