from ipynbsrv.contract.services import ContainerHostSelectionService


class PrimitiveContainerHostSelectionService(ContainerHostSelectionService):
    '''
    Very primitive round robin approach for selecting a host for a new container
    '''

    last = 0

    @staticmethod
    def get_server(self, count):
        if count == 1:
            return 0
        else:
            next = (self.last + 1) % count
            self.last = next
            return next
