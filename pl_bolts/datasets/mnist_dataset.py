from pl_bolts.utils import _PIL_AVAILABLE, _TORCHVISION_AVAILABLE
from pl_bolts.utils.warnings import warn_missing_pkg

if _TORCHVISION_AVAILABLE:
    from torchvision import transforms as transform_lib
    from torchvision.datasets import MNIST
else:  # pragma: no cover
    warn_missing_pkg('torchvision')
    MNIST = object

if _PIL_AVAILABLE:
    from PIL import Image
else:  # pragma: no cover
    warn_missing_pkg('PIL', pypi_name='Pillow')


class BinaryMNIST(MNIST):
    def __getitem__(self, idx):
        """
        Args:
            index (int): Index
        Returns:
            tuple: (image, target) where target is index of the target class.
        """
        img, target = self.data[idx], int(self.targets[idx])

        # doing this so that it is consistent with all other datasets
        # to return a PIL Image
        img = Image.fromarray(img.numpy(), mode='L')

        if self.transform is not None:
            img = self.transform(img)

        if self.target_transform is not None:
            target = self.target_transform(target)

        # binary
        img[img < 0.5] = 0.0
        img[img >= 0.5] = 1.0

        return img, target
