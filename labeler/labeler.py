# Copyrights rostepifanov.ru
#   Author: Rostislav Epifanov
#   Created: 13/07/2020

import pandas as pd

from pathlib import Path
from IPython.display import display, clear_output
from ipywidgets import (BoundedIntText, Text, Label, Textarea,
                        Button, Dropdown, Checkbox,
                        Layout, HBox, VBox)


class Labeler(object):
    """Class create widget to label data
    """

    def __init__(self, data, lines_per_pages=30):
        """
        :param self:
        :param data: messages
        """
        self.__data = data

        self.__current_page = 0
        self.__lines_per_pages = lines_per_pages
        self.__total_pages = (self.__data.shape[0] + self.__lines_per_pages - 1) // self.__lines_per_pages

        self.__classes_decent_map = ['unmarked', 'decent', 'obscene', 'skipped']
        self.__classes_moral_map = ['unmarked', 'moral', 'immoral', 'skipped']
        self.__classes_person_map = ['unmarked', 'person insult', 'imperson insult', 'skipped']

        self.__classes_decent_map = dict(zip( self.__classes_decent_map, range(4)))
        self.__classes_moral_map = dict(zip( self.__classes_moral_map, range(4)))
        self.__classes_person_map = dict(zip( self.__classes_person_map, range(4)))

        self.__decent_key = 'dropbox_decent_{}'
        self.__moral_key = 'dropbox_moral_{}'
        self.__person_key = 'dropbox_person_{}'

        self.__message2class_map = { idx: [0, 0, 0] for idx, _ in enumerate(data['message']) }

    def __setup_navigation_gui(self):
        """Create gui to manage message displaying

        :param self:

        :return:
            created gui, gui variable params, controllers
        """

        hbox_layout = Layout(align_self='center',
                             margin='0px 0px 10px 0')

        field_layout = Layout(width='100px', align_self='center')
        button_layout = Layout(width='200px')

        page_field = Label(layout=field_layout)  

        next_button = Button(description='Следующая',
                             layout=button_layout,
                            )

        previous_button = Button(description='Предыдущая',
                                 layout=button_layout,
                                )

        gui = HBox([previous_button, page_field, next_button], layout = hbox_layout)

        params = {'page_field': page_field,
                 }

        controllers = {'next_button': next_button,
                       'previous_button': previous_button,
                      }

        return gui, params, controllers


    def __setup_window_gui(self):
        """Create gui to display messages

        :param self:

        :return:
            created gui, gui variable params, controllers
        """
        controllers = dict()

        HBoxes = list()

        hbox_layout = Layout(border='solid',
                             margin='0px 0px 10px 0px')

        field_layout = Layout(width='80%', height='75px')
        dropbox_layout = Layout(width='150px')

        classes_layout = Layout(width='20%')

        lbound = self.__current_page * self.__lines_per_pages
        rbound = min(lbound + self.__lines_per_pages, self.__data.shape[0])

        for idx in range(lbound, rbound):
            message_field = Textarea( value=self.__data['message'][idx],
                                      layout = field_layout
                                    )

            decent_dropbox = Dropdown( options=list(self.__classes_decent_map.items()),
                                       value=0,
                                       layout = dropbox_layout
                                     )

            moral_dropbox = Dropdown( options=list(self.__classes_moral_map.items()),
                                       value=0,
                                       layout = dropbox_layout
                                     )

            person_dropbox = Dropdown( options=list(self.__classes_person_map.items()),
                                       value=0,
                                       layout = dropbox_layout
                                     )

            controllers[self.__decent_key.format(idx)] = decent_dropbox
            controllers[self.__moral_key.format(idx)] = moral_dropbox
            controllers[self.__person_key.format(idx)] = person_dropbox

            classes = VBox([decent_dropbox, moral_dropbox, person_dropbox], layout=classes_layout)

            message_box = HBox([message_field, classes], layout=hbox_layout)
            HBoxes.append(message_box)

        gui = VBox(HBoxes)

        return gui, dict(), controllers

    def __setup_page_field(self, page_field):
        """Set up page field 

        :param self:
        :param page_field: 


        :return: 
        """

        page_field.value = '{} из {}'.format(self.__current_page + 1, self.__total_pages)

    def __setup_dropbox_callbacks(self, dropboxes):
        """Set up dropbox callbacks 

        :param self:
        :param page_field: 


        :return: 
        """

        def dropbox_callback(miner, idx, pos):
            def controller(dropbox):
                if dropbox['type'] == 'change' and dropbox['name'] == 'value':
                    self.__message2class_map[idx][pos] = dropbox['new']

            return controller

        lbound = self.__current_page * self.__lines_per_pages
        rbound = min(lbound + self.__lines_per_pages, self.__data.shape[0])

        for idx in range(lbound, rbound):
            for pos, key in zip([0, 1, 2], [ self.__decent_key, self.__moral_key, self.__person_key ]):
                dropbox = dropboxes[key.format(idx)]
                dropbox.observe(dropbox_callback(self, idx, pos))
                dropbox.value = self.__message2class_map[idx][pos]


    def __setup_button_callbacks(self, gui, controllers, dropboxes, params):
        """Set up button callbacks 

        :param self:
        :param gui: gui to display
        :param controllers: expect to use 'next_button' and 'previous_button'
        :param dropboxes: 
        :param params: expect to use 'page_field'


        :return: 
        """

        def next_button_predicate(labeler):
            if labeler.__current_page < labeler.__total_pages - 1:
                labeler.__current_page += 1
                return True
            else:
                return False

        def previous_button_predicate(labeler):
            if labeler.__current_page > 0:
                labeler.__current_page -= 1
                return True
            else:
                return False

        def button_callback(labeler, gui, params, dropboxes, predicate):
            def controller(button):
                if (predicate(labeler)):
                    window_gui, _, dropboxes = labeler.__setup_window_gui()

                    labeler.__setup_dropbox_callbacks(dropboxes)
                    labeler.__setup_page_field(params['page_field'])

                    gui_layers = list(gui.children)
                    gui_layers[1] = window_gui
                    gui.children = gui_layers

                    clear_output()
                    display(gui)

            return controller

        controllers['next_button'].on_click(button_callback(self, gui, params, dropboxes, next_button_predicate))
        controllers['previous_button'].on_click(button_callback(self, gui, params, dropboxes, previous_button_predicate))


    def run_labeler_gui(self, ):
        """Run answer miner gui controller

        :param self:

        :return: 
        """

        navigation_gui, params, controllers = self.__setup_navigation_gui()
        window_gui, _, dropboxes = self.__setup_window_gui()
        gui = VBox([navigation_gui, window_gui, navigation_gui])

        self.__setup_button_callbacks(gui, controllers, dropboxes, params)
        self.__setup_page_field(params['page_field'])
        self.__setup_dropbox_callbacks(dropboxes)

        display(gui)


    def load(self, filepath: Path):
        """Load labeled data from file

        :param self:
        :param filepath: path to load labels

        :return:
        """

        self.__data = pd.read_csv(filepath, index_col=0)

        decent, moral, person = self.__data.decent.values, self.__data.moral.values, self.__data.person.values

        for idx, (ldecent, lmoral, lperson) in enumerate(zip(decent, moral, person)):
            self.__message2class_map[idx] = [ self.__classes_decent_map[ldecent],
                                              self.__classes_moral_map[lmoral],
                                              self.__classes_person_map[lperson] ]

    def store(self, filepath: Path):
        """Store labeled data to file

        :param self:
        :param filepath: path to store labels

        :return:
        """

        iclasses_decent_map = {value: key for key, value in self.__classes_decent_map.items()}
        iclasses_moral_map = {value: key for key, value in self.__classes_moral_map.items()}
        iclasses_person_map = {value: key for key, value in self.__classes_person_map.items()}

        alabels = list()

        labeled_data = pd.DataFrame(self.__data)

        for idx, label in self.__message2class_map.items():
            labels = ( iclasses_decent_map[label[0]],
                       iclasses_moral_map[label[1]],
                       iclasses_person_map[label[2]] )

            alabels.append(labels)

        alabels = pd.DataFrame(alabels, columns=['decent', 'moral', 'person']) 
        labeled_data = pd.concat([labeled_data, alabels], axis=1, sort=False)
        labeled_data.to_csv(filepath, index=True)
