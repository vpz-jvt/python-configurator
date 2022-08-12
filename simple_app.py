#region Table

from kivy.metrics import dp

from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.screen import MDScreen

# Adjusting example using .csv table.
import pandas as pd
from array import ArrayType

csv_table = pd.read_csv('data/Example_table.csv', sep = ';', decimal='.')
cols = csv_table.columns

class Example(MDApp):
    """ Simple Exemple class to use Kivy MD

    Parameters
    ----------
    MDApp : kivymd.app.MDApp
        Aplication class of kivymd
    """
    def build(self) -> MDScreen:
        """
        Initializes the application; it will be called only once. 
        If this method returns a widget (tree), it will be used as the root widget and added to the window.

        Returns
        -------
        MDScreen
            Screen is an element intended to be used with a ~kivymd.uix.screenmanager.MDScreenManager.
        """
        self.data_tables = MDDataTable(
            use_pagination=True,
            check=True,
            column_data=[
                (cols[0], dp(30)),
                (cols[1], dp(30)),
                (cols[2], dp(60), self.sort_on_signal),
                (cols[3], dp(30)),
                (cols[4], dp(30)),
                (cols[5], dp(30), self.sort_on_schedule),
                (cols[6], dp(30), self.sort_on_team),
            ],
            row_data=csv_table.to_records(index=False),
            sorted_on="Schedule",
            sorted_order="ASC",
            elevation=2,
        )
        self.data_tables.bind(on_row_press=self.on_row_press)
        self.data_tables.bind(on_check_press=self.on_check_press)
        screen = MDScreen()
        screen.add_widget(self.data_tables)
        return screen

    def on_row_press(self, instance_table, instance_row):
        '''Called when a table row is clicked.'''

        print(instance_table, instance_row)

    def on_check_press(self, instance_table, current_row):
        '''Called when the check box in the table row is checked.'''

        print(instance_table, current_row)

    # Sorting Methods:
    # since the https://github.com/kivymd/KivyMD/pull/914 request, the
    # sorting method requires you to sort out the indexes of each data value
    # for the support of selections.
    #
    # The most common method to do this is with the use of the builtin function
    # zip and enumerate, see the example below for more info.
    #
    # The result given by these funcitons must be a list in the format of
    # [Indexes, Sorted_Row_Data]

    def sort_on_signal(self, data: ArrayType) -> ArrayType:
        """ Method to sort column by its values

        Parameters
        ----------
        data : Arraytype
            Column to be sorted.

        Returns
        -------
        ArrayType
            Sorted Column
        """
        return zip(*sorted(enumerate(data), key=lambda l: l[1][2]))

    def sort_on_schedule(self, data: ArrayType) -> ArrayType:
        """ Method to sort column by its values

        Parameters
        ----------
        data : Arraytype
            Column to be sorted.

        Returns
        -------
        ArrayType
            Sorted Column
        """
        return zip(
            *sorted(
                enumerate(data),
                key=lambda l: sum(
                    [
                        int(l[1][-2].split(":")[0]) * 60,
                        int(l[1][-2].split(":")[1]),
                    ]
                ),
            )
        )

    def sort_on_team(self, data: ArrayType) -> ArrayType:
        """ Method to sort column by its values

        Parameters
        ----------
        data : Arraytype
            Column to be sorted.

        Returns
        -------
        ArrayType
            Sorted Column
        """
        return zip(*sorted(enumerate(data), key=lambda l: l[1][-1]))


Example().run()

#endregion