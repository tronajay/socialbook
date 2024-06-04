from rest_framework import viewsets

class ViewSetMod(viewsets.ViewSet):

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context