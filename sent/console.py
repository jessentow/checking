#!/usr/bin/python3
""" HBNBCommand class definition """
import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.state import State
from models.user import User
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """
    HBNBCommand class   the entry point of the command interpreter
    """

    prompt = '(hbnb) '

    __cls = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Place": Place,
        "Amenity": Amenity,
        "Review": Review
        }

    def emptyline(self):
        """Do nothing if empty line + enter hit"""
        return False

    """-------COMMANDS------"""

    def do_EOF(self, line):
        """EOF command to exit the program
        """
        return True

    def do_quit(self, line):
        """Quit command to exit the program
        """
        return True

    def do_create(self, line):
        """Creates a new instance of BaseModel
                -save it
                -print the id
        """
        line = line.split(' ')
        if not line[0]:
            print('** class name missing **')
        elif line[0] not in __class__.__cls:
            print('** class doesn\'t exist **')
        else:
            instance = __class__.__cls[line[0]]()
            print(instance.id)
            instance.save()

    def do_show(self, line):
        """Prints the string representation of an instance based on:
            - The class name
            - Id
        """
        line = line.split(' ')
        all_instances = storage.all()

        if not line[0]:
            print('** class name missing **')
            return
        elif line[0] not in __class__.__cls:
            print('** class doesn\'t exist **')
            return

        try:
            cls_id = '{}.{}'.format(line[0], line[1])
            if cls_id not in all_instances:
                print('** no instance found **')
            else:
                print(all_instances[cls_id])
        except IndexError:
            print('** instance id missing **')

    def do_destroy(self, line):
        """Deletes an instance based on:
            - The class name
            - Id
        """
        line = line.split(' ')
        all_instances = storage.all()

        if not line[0]:
            print('** class name missing **')
            return
        elif line[0] not in __class__.__cls:
            print('** class doesn\'t exist **')
            return

        try:
            cls_id = '{}.{}'.format(line[0], line[1])
            if cls_id not in all_instances:
                print('** no instance found **')
            else:
                del all_instances[cls_id]
                storage.save()
        except IndexError:
            print('** instance id missing **')

    def do_all(self, line):
        """Prints all string representation of all instances
        """

        all_instances = storage.all()
        li = []
        st = ''
        if line:
            line = line.split(' ')

            if line[0] not in __class__.__cls:
                print('** class doesn\'t exist **')
                return
            else:

                for k in all_instances.values():
                    if k.__class__.__name__ == line[0]:
                        st = str(k)
                        li.append(st)
                print(li)
        else:

            for k in all_instances.values():
                st = str(k)
                li.append(st)

            print(li)

    def do_update(self, line):
        """Updates an instance based on:
            - The class name
            - Id
        """
        line = split(line, ' ')
        all_instances = storage.all()

        if len(line) == 0:
            print("** class name missing **")
            return False
        if line[0] not in HBNBCommand.__cls:
            print("** class doesn't exist **")
            return False
        if len(line) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(line[0], line[1]) not in all_instances.keys():
            print("** no instance found **")
            return False
        if len(line) == 2:
            print("** attribute name missing **")
            return False
        if len(line) == 3:
            try:
                type(eval(line[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        cls_id = "{}.{}".format(line[0], line[1])
        obj = all_instances[cls_id]

        if len(line) == 4:
            if line[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[line[2]])
                obj.__dict__[line[2]] = valtype(line[3])
            else:
                obj.__dict__[line[2]] = line[3]
        elif type(eval(line[2])) == dict:
            typ = [str, int, float]
            for k, v in eval(line[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in typ):
                    valtype = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = valtype(v)
                else:
                    obj.__dict__[k] = v
        storage.save()

    def default(self, line):
        """Retrieve all instances of a class
        """
        methods = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }

        match = re.search(r"\.", line)

        if match is not None:
            argl = [line[:match.span()[0]], line[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", argl[1])
            if match is not None:
                command = [argl[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in methods.keys():
                    call = "{} {}".format(argl[0], command[1])
                    return methods[command[0]](call)

        return False

    def do_count(self, line):
        """Retrieve the number of instances of a class
        """
        coun = 0
        line = split(line, " ")

        all_instances = storage.all()
        for key in all_instances:
            name = key.split('.')
            if name[0] == line[0]:
                coun += 1
        print(coun)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
