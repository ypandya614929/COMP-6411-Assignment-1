#!/usr/bin/python
# -*- coding: utf-8 -*-

# ----- Program Details -----
# Age is always integer and phone number is in XXX XXX-XXXX format is accepted.
# Further options are given when entering wrong data/info to help the client user.

# The socket module is a framework for creating network servers.
# It defines classes for handling synchronous network requests
import socket
# The JSON module is mainly used to convert the python dictionary above
# into a JSON string that can be transmitted over the network
import json

HOST_NAME = 'localhost'
PORT = 9999
BUFF_SIZE = 65536


class ClientOperations:
    """
    A class used to represent all the client side operations

    Methods
    -------
    general_print_fun(print_var)
        It is a general printing method that beautifies print(statement
    input_list()
        It is a general input/menu method
    get_input(field_name='')
        It is a general method to take any input and display input message
        based on parameter
    print_report(res_data_dict)
        It display customer data based on response from the server
    print_response(data_dict)
        It takes response from the server and display to client accordingly
    validate_age(age)
        It takes age and return True or False based on validation
    validate_name(name)
        It takes name and return True or False based on validation
    validate_phone(phone)
        It takes phone and return True or False based on validation
    """

    @staticmethod
    def general_print_fun(print_var):
        """It is a general printing method that beautifies print(statement
        according to given value of the parameter

        Parameters
        ----------
        print_var : str
            The printing value

        """
        print('---------------------------------')
        print(print_var)
        print('---------------------------------')

    @staticmethod
    def input_list():
        """It is a general input/menu method

        Returns
        -------
        str
            a string containing selected option
        """
        print('\nPython DB Menu')
        print('1. Find customer')
        print('2. Add customer')
        print('3. Delete customer')
        print('4. Update customer age')
        print('5. Update customer address')
        print('6. Update customer phone')
        print('7. Print report')
        print('8. Exit')

        choice = input('Select: ')

        return choice

    @staticmethod
    def sub_input_list():
        """It is a general sub input/menu method

        Returns
        -------
        str
            a string containing selected option
        """
        print('1. Do you want to Re-enter')
        print('2. Exit')

        choice = input('Select: ')

        return choice

    @staticmethod
    def get_input(field_name=''):
        """It is a general method to take any input and display
        input message based on parameter

        Parameters
        ----------
        field_name : str
            The field_name to display beautifully

        Returns
        -------
        str
            a string that contains input from the user
        """
        label = 'Enter customer {} : '.format(field_name)
        key = input(label)
        return key

    @staticmethod
    def print_report(res_data_dict):
        """It display customer data based on response from the server

        Parameters
        ----------
        res_data_dict : dict
            The dictionary containing customer data
        """
        print('---------------------------------------------------------------------------------------------------')
        print('{:<25}{:<10}{:<50}{:<}'.format('name', 'age', 'address',
                                             'phone'))
        print('---------------------------------------------------------------------------------------------------')

        for (key, value_dict) in res_data_dict.items():
            name = key
            age = value_dict.get('age', '')
            address = value_dict.get('address', '')
            phone = value_dict.get('phone', '')
            print('{:<25}{:<10}{:<50}{:<}'.format(name, age, address,
                                                 phone))

        print('---------------------------------------------------------------------------------------------------')

    @staticmethod
    def print_response(data_dict):
        """It takes response from the server and display to client accordingly

        Parameters
        ----------
        data_dict : dict
            The dictionary contains the success/error message received
            from the server
        """
        if data_dict.get('message'):
            ClientOperations().general_print_fun(data_dict['message'])
        else:
            print('---------------------------------------------------------------------------------------------------')
            print('{:<25}{:<10}{:<50}{:<}'.format('name', 'age', 'address', 'phone'))
            print('---------------------------------------------------------------------------------------------------')

            name = data_dict.get('name')
            age = data_dict.get('age', '')
            address = data_dict.get('address', '')
            phone = data_dict.get('phone', '')
            print('{:<25}{:<10}{:<50}{:<}'.format(name, age, address, phone))

            print('---------------------------------------------------------------------------------------------------')

    @staticmethod
    def validate_age(age):
        """It takes age and return True or False based on validation

        Parameters
        ----------
        age : str
            The age of customer

        Returns
        -------
        boolean
        """
        if age:
            try:
                age = int(age)
                if age <= 0:
                    ClientOperations().general_print_fun("Age can't be 0, Please enter valid age")
                    return False
            except Exception:
                ClientOperations().general_print_fun("Please enter valid age")
                return False
        return True

    @staticmethod
    def validate_name(name):
        """It takes name and return True or False based on validation

        Parameters
        ----------
        name : str
            The name of customer

        Returns
        -------
        boolean
        """
        if name:
            return True
        ClientOperations().general_print_fun("Please provide Customer name")
        return False

    @staticmethod
    def validate_phone(phone):
        """It takes phone and return True or False based on validation

        Parameters
        ----------
        phone : str
            The phone of customer

        Returns
        -------
        boolean
        """
        if phone:
            try:
                phone_list = phone.split(" ")
                if len(phone_list[0]) == 3:
                    phone_list[0] = int(phone_list[0])
                else:
                    ClientOperations().general_print_fun(
                        "Please enter valid phone in XXX XXX-XXXX format or press Enter to leave it empty")
                    return False
                phone_list = phone_list[1].split("-")
                if len(phone_list[0]) == 3:
                    phone_list[0] = int(phone_list[0])
                else:
                    ClientOperations().general_print_fun(
                        "Please enter valid phone in XXX XXX-XXXX format or press Enter to leave it empty")
                    return False
                if len(phone_list[1]) == 4:
                    phone_list[1] = int(phone_list[1])
                else:
                    ClientOperations().general_print_fun(
                        "Please enter valid phone in XXX XXX-XXXX format or press Enter to leave it empty")
                    return False
            except Exception:
                ClientOperations().general_print_fun(
                    "Please enter valid phone in XXX XXX-XXXX format or press Enter to leave it empty")
                return False
        return True


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST_NAME, PORT))

    clientOperations = ClientOperations()

    def fetch_data(sock):
        """It takes socket object and returns the data sent by server
        this method is in use when data/package length is more than BUFF_SIZE

        Parameters
        ----------
        sock : socket
            The socket class object

        Returns
        -------
        bytes
            a byte string containing the response from the server
        """
        data_dict = b''
        while True:
            packet = sock.recv(BUFF_SIZE)
            data_dict += packet
            if BUFF_SIZE > len(packet):
                break
        return data_dict


    isExit = False

    while not isExit:

        # menu
        choice = clientOperations.input_list().strip()

        if choice in ['1', 1]:
            # To find customer data
            is_sendto = True
            name = clientOperations.get_input('name').strip()
            while not clientOperations.validate_name(name):
                choice_1 = clientOperations.sub_input_list().strip()
                if choice_1 in ['2', 2]:
                    is_sendto = False
                    break
                name = clientOperations.get_input('name').strip()
            if is_sendto:
                req_dict = {'choice': choice, 'name': name}
                sock.sendall(json.dumps(req_dict).encode('utf-8'))
                res_data_dict = json.loads(sock.recv(BUFF_SIZE).decode('utf-8'))
                clientOperations.print_response(res_data_dict)

        elif choice in ['2', 2]:
            # To add customer data
            is_sendto = True
            name = clientOperations.get_input('name').strip()
            while not clientOperations.validate_name(name):
                choice_1 = clientOperations.sub_input_list().strip()
                if choice_1 in ['2', 2]:
                    is_sendto = False
                    break
                name = clientOperations.get_input('name').strip()
            if is_sendto:
                age = clientOperations.get_input('age or press Enter to leave it empty').strip()
                while not clientOperations.validate_age(age):
                    choice_1 = clientOperations.sub_input_list().strip()
                    if choice_1 in ['2', 2]:
                        is_sendto = False
                        break
                    age = clientOperations.get_input('age or press Enter to leave it empty').strip()
            if is_sendto:
                address = clientOperations.get_input('address or press Enter to leave it empty').strip()
                phone = clientOperations.get_input(
                    'phone in XXX XXX-XXXX format or press Enter to leave it empty').strip()
                while not clientOperations.validate_phone(phone):
                    choice_1 = clientOperations.sub_input_list().strip()
                    if choice_1 in ['2', 2]:
                        is_sendto = False
                        break
                    phone = clientOperations.get_input(
                        'phone in XXX XXX-XXXX format or press Enter to leave it empty').strip()
            if is_sendto:
                req_dict = {
                    'choice': choice,
                    'name': name,
                    'age': age,
                    'address': address,
                    'phone': phone,
                }
                sock.sendall(json.dumps(req_dict).encode('utf-8'))
                res_data_dict = json.loads(sock.recv(BUFF_SIZE).decode('utf-8'))
                clientOperations.print_response(res_data_dict)

        elif choice in ['3', 3]:
            # To delete specific customer data
            is_sendto = True
            name = clientOperations.get_input('name').strip()
            while not clientOperations.validate_name(name):
                choice_1 = clientOperations.sub_input_list().strip()
                if choice_1 in ['2', 2]:
                    is_sendto = False
                    break
                name = clientOperations.get_input('name').strip()
            if is_sendto:
                req_dict = {'choice': choice, 'name': name}
                sock.sendall(json.dumps(req_dict).encode('utf-8'))
                res_data_dict = json.loads(sock.recv(BUFF_SIZE).decode('utf-8'))
                clientOperations.print_response(res_data_dict)

        elif choice in ['4', 4]:
            # To update customer age
            is_sendto = True
            name = clientOperations.get_input('name').strip()
            while not clientOperations.validate_name(name):
                choice_1 = clientOperations.sub_input_list().strip()
                if choice_1 in ['2', 2]:
                    is_sendto = False
                    break
                name = clientOperations.get_input('name').strip()
            if is_sendto:
                age = clientOperations.get_input('age or press Enter to leave it empty').strip()
                while not clientOperations.validate_age(age):
                    choice_1 = clientOperations.sub_input_list().strip()
                    if choice_1 in ['2', 2]:
                        is_sendto = False
                        break
                    age = clientOperations.get_input('age or press Enter to leave it empty').strip()
            if is_sendto:
                req_dict = {'choice': choice, 'name': name, 'age': age}
                sock.sendall(json.dumps(req_dict).encode('utf-8'))
                res_data_dict = json.loads(sock.recv(BUFF_SIZE).decode('utf-8'))
                clientOperations.print_response(res_data_dict)

        elif choice in ['5', 5]:
            # To update customer address
            is_sendto = True
            name = clientOperations.get_input('name').strip()
            while not clientOperations.validate_name(name):
                choice_1 = clientOperations.sub_input_list().strip()
                if choice_1 in ['2', 2]:
                    is_sendto = False
                    break
                name = clientOperations.get_input('name').strip()
            address = clientOperations.get_input('address or press Enter to leave it empty').strip()
            req_dict = {'choice': choice, 'name': name,
                        'address': address}
            sock.sendall(json.dumps(req_dict).encode('utf-8'))
            res_data_dict = json.loads(sock.recv(BUFF_SIZE).decode('utf-8'))
            clientOperations.print_response(res_data_dict)

        elif choice in ['6', 6]:
            # To update customer phone
            is_sendto = True
            name = clientOperations.get_input('name').strip()
            while not clientOperations.validate_name(name):
                choice_1 = clientOperations.sub_input_list().strip()
                if choice_1 in ['2', 2]:
                    is_sendto = False
                    break
                name = clientOperations.get_input('name').strip()
            if is_sendto:
                phone = clientOperations.get_input(
                    'phone in XXX XXX-XXXX format or press Enter to leave it empty').strip()
                while not clientOperations.validate_phone(phone):
                    choice_1 = clientOperations.sub_input_list().strip()
                    if choice_1 in ['2', 2]:
                        is_sendto = False
                        break
                    phone = clientOperations.get_input(
                        'phone in XXX XXX-XXXX format or press Enter to leave it empty').strip()
            if is_sendto:
                req_dict = {'choice': choice, 'name': name, 'phone': phone}
                sock.sendall(json.dumps(req_dict).encode('utf-8'))
                res_data_dict = json.loads(sock.recv(BUFF_SIZE).decode('utf-8'))
                clientOperations.print_response(res_data_dict)

        elif choice in ['7', 7]:
            # To sort and return customer data
            req_dict = {'choice': choice}
            sock.sendall(json.dumps(req_dict).encode('utf-8'))
            res_data_dict = json.loads(fetch_data(sock).decode('utf-8'))
            clientOperations.print_report(res_data_dict)

        elif choice in ['8', 8]:
            # To exit the client app
            clientOperations.general_print_fun('GoodBye')
            isExit = True
        else:
            # check for invalid selection
            clientOperations.general_print_fun('Select valid option')

    if isExit:
        sock.close()
