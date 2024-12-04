class Observer:
    def update(self, event):
        raise NotImplementedError("Subclass must implement 'update'")