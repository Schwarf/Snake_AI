import torch
import torch.nn.functional as F
import os


class Linear_QNet(torch.nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self._input_layer = torch.nn.Linear(input_size, hidden_size)
        self._output_layer = torch.nn.Linear(hidden_size, output_size)

    def forward(self, input_tensor):
        next_layer = F.relu(self._input_layer(input_tensor))
        next_layer = F.relu(self._output_layer(next_layer))
        return next_layer

    def save(self, file_name='model.pth'):
        model_folder_path = './model'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)
        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name)



