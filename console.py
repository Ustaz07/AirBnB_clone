#!/usr/bin/python3
""" Console Module """
import cmd
import sys
from models.base_model import BaseModel
from models.__init__ import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """ Contains the functionality for the HBNB console"""

    prompt = '(hbnb) ' if sys.__stdin__.isatty() else ''

    classes = {
        'BaseModel': BaseModel, 'User': User, 'Place': Place,
        'State': State, 'City': City, 'Amenity': Amenity,
        'Review': Review
    }
    dot_cmds = ['all', 'count', 'show', 'destroy', 'update']
    types = {
        'number_rooms': int, 'number_bathrooms': int,
        'max_guest': int, 'price_by_night': int,
        'latitude': float, 'longitude': float
    }

    def preloop(self):
        if not sys.__stdin__.isatty():
            print('(hbnb)')

    def postcmd(self, stop, line):
        if not sys.__stdin__.isatty():
            print('(hbnb) ', end='')
        return stop

    def do_quit(self, command):
        exit()

    def do_EOF(self, arg):
        print()
        exit()

    def emptyline(self):
        pass

    def do_create(self, args):
        if not args:
            print("** class name missing **")
            return
        elif args not in self.classes:
            print("** class doesn't exist **")
            return
        new_instance = self.classes[args]()
        storage.save()
        print(new_instance.id)

    def do_show(self, args):
        if not args:
            print("** class name missing **")
            return
        class_name, obj_id = self.parse_args(args, 2)
        if not class_name or not obj_id:
            return
        key = "{}.{}".format(class_name, obj_id)
        if key not in storage.all():
            print("** no instance found **")
        else:
            print(storage.all()[key])

    def do_destroy(self, args):
        class_name, obj_id = self.parse_args(args, 2)
        if not class_name or not obj_id:
            return
        key = "{}.{}".format(class_name, obj_id)
        if key not in storage.all():
            print("** no instance found **")
        else:
            del storage.all()[key]
            storage.save()

    def do_all(self, args):
        if args:
            class_name, _ = self.parse_args(args, 1)
            if not class_name:
                return
            print([str(obj) for key, obj in storage.all().items() if key.startswith(class_name + '.')])
        else:
            print([str(obj) for obj in storage.all().values()])

    def do_count(self, args):
        class_name, _ = self.parse_args(args, 1)
        if not class_name:
            return
        count = sum(1 for key in storage.all().keys() if key.startswith(class_name + '.'))
        print(count)

    def do_update(self, args):
        class_name, obj_id, *update_args = self.parse_args(args, 3)
        if not class_name or not obj_id or not update_args:
            return
        key = "{}.{}".format(class_name, obj_id)
        if key not in storage.all():
            print("** no instance found **")
            return
        obj = storage.all()[key]
        for i in range(0, len(update_args), 2):
            attr_name = update_args[i]
            if attr_name in self.types:
                attr_val = self.types[attr_name](update_args[i + 1])
            else:
                attr_val = update_args[i + 1]
            setattr(obj, attr_name, attr_val)
        storage.save()

    def parse_args(self, args, num_args):
        args_list = args.split()
        if len(args_list) < num_args:
            print("** class name missing **" if len(args_list) == 0 else "** instance id missing **")
            return None, None
        return args_list[0], args_list[1]


if __name__ == "__main__":
    HBNBCommand().cmdloop()

