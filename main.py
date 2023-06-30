from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.pickers import MDTimePicker
from datetime import datetime


from kivymd.uix.list import TwoLineAvatarIconListItem,ILeftBody
from kivymd.uix.selectioncontrol import MDCheckbox


from database import Database
# Instantiating the Database class by creating db object
db = Database()
db.create_task_table()

class DialogContent(MDBoxLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.ids.date_text.text = datetime.now().strftime("%A %d %B %Y") 
        self.ids.time_label.text = datetime.now().strftime("%H:%M:%S")
        # This func will show the date picker
        
    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save= self.on_save)
        date_dialog.open()
     
     
    def show_time_picker(self):
        time_dialog = MDTimePicker()
        time_dialog.bind(time = self.on_sav)
        time_dialog.open()
        
    # def on_cancel(self, instance , time):
    #     self.ids.time_label.text       
            
        # This fucntion will get the date and saves in a friendly form
    def on_sav(self,intstance, time_range):
        self.ids.time_label.text = str(time_range.strftime("%H:%M:%S"))
           
    def on_save(self, instance, value, date_range):
        date = value.strftime("%A %d %B %Y") 
        self.ids.date_text.text = str(date)
  
  
# Class for marking and deleting the element
class ListItemWithCheckbox(TwoLineAvatarIconListItem):
    def __init__(self, pk = None, **kwargs):
        super().__init__(**kwargs)
        self.pk = pk
  # Marking the item as complete or incomplete
    def mark(self, check, the_list_item):
        if check.active == True:
            the_list_item.text = '[s]'+ the_list_item.text + '[/s]'
            db.mark_task_as_completed(the_list_item.pk)
        else:
            the_list_item.text = "[b]"+str(db.mark_task_as_incompleted(the_list_item.pk)) + "[/b]"

    # Deleting the list item    
    def delete_item(self, the_list_item):
        self.parent.remove_widget(the_list_item)
        db.delete_task(the_list_item.pk)
  
  
class LeftCheckbox(ILeftBody,MDCheckbox):
    pass

  
            
class MainApp(MDApp):
    task_list_dialog = None
    
    # this is the function for setting the theme
    def build(self):
        self.theme_cls.theme_style="Light"
        self.theme_cls.primary_palette = "Purple"
        
    #this is the show task function

    def show_task_dialog(self):
        if not self.task_list_dialog:
            self.task_list_dialog = MDDialog(
                title = 'Create Task',
                type = 'custom',
                content_cls = DialogContent(),
            )

        self.task_list_dialog.open()
            
    # adding tasks
    def add_task(self,task,task_date,task_time):
        print(task_time)
        created_task = db.create_task(task.text , task_date)
        self.root.ids['container'].add_widget(ListItemWithCheckbox(pk = created_task[0], text = '[b]'+ created_task[1] + '[/b]', secondary_text = created_task[2]))
        task.text = ""
                                                                   
        # self.root.ids['container'].add_widget(ListItemWithCheckbox(text = '[b]'+ task.text + '[/b]', secondary_text = task_date))
    
            
    def close_dialog(self, *args):
        self.task_list_dialog.dismiss()
        

    def on_start(self):
        '''This is to load the saved tasks and add them tothe MDList widget'''
        completed_task, incompleted_task = db.get_task()

        if incompleted_task != []:
            for task in incompleted_task:
                add_task = ListItemWithCheckbox(pk = task[0], text = task[1], secondary_text = task[2])
                self.root.ids.container.add_widget(add_task)
        
        if completed_task != []:

            for task in completed_task:
                add_task = ListItemWithCheckbox(pk = task[0], text = '[s]'+task[1]+'[/s]' , secondary_text = task[2])

                add_task.ids.check.active = True
                self.root.ids.container.add_widget(add_task)

           
    





if __name__ == '__main__':
    app = MainApp()
    app.run()


