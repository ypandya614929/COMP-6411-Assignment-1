#!/usr/bin/python
# -*- coding: utf-8 -*-

# ----- Program Details -----
# For Initial data read from the file only age field validation is applied. No phone number validation is added.
# Program works in Case Sensitive manner.
# Server only returns the data/errors all printing related commands are operated by client.

# The SocketServer module is a framework for creating network servers.
# It defines classes for handling synchronous network requests
import socketserver
# The JSON module is mainly used to convert the python dictionary above
# into a JSON string that can be transmitted over the network
import json
import socket

class ServerOperations:
    """
    A class used to represent all the server side operations

    ...
    Attributes
    ----------
    database_dict : dict
        a dictionary which contains the customer data

    Methods
    -------
    get_customer(self, name='')
        It takes customer name and return customer detail if exists
        Otherwise return error message
    add_customer(self, name='', age='', address='', phone='')
        It takes customer details to store the data into server if 
        name is not already exists and return the success message
        Otherwise return error message
    delete_customer(self, name='')
        It takes customer name to remove the customer data from the 
        server if name is already exists and return the success message
        Otherwise return error message
    update_customer_age(self, name='', age='')
        It takes customer name and age to update the customer age if 
        customer name is already exists and return the success message
        Otherwise return error message
    update_customer_address(self, name='', address='')
        It takes customer name and address to update the customer address if 
        customer name is already exists and return the success message
        Otherwise return error message
    update_customer_phone(self, name='', phone='')
        It takes customer name and phone to update the customer phone if 
        customer name is already exists and return the success message
        Otherwise return error message
    sort_database(self)
        It sorts the customer data based on customer name
    read_file(self, path_name='data.txt')
        It takes file path and load the customer data into the server
    """

    database_dict = {}

    def __init__(self):
        self.database_dict = {}
        self.read_file()
        print("Data successfully loaded into server !")

    def get_customer(self, name=''):
        """It takes customer name and return customer detail if exists
        Otherwise return error message

        Parameters
        ----------
        name : str
            The name of the customer

        Returns
        -------
        dict
            a dict of customer record if customer name is exists
            Otherwise return error message
        """
        if name:
            if self.database_dict.get(name):
                ans_dict = self.database_dict[name]
            else:
                ans_dict = {'message': 'Customer not found'}
        else:
            ans_dict = {'message': 'Please provide Customer name'}
        return ans_dict

    def add_customer(self, name='', age='', address='', phone=''):
        """It takes customer details to store the data into server if 
        name is not already exists and return the success message
        Otherwise return error message

        Parameters
        ----------
        name : str
            The name of the customer
        age : str
            The age of the customer
        address : str
            The address of the customer
        phone : str
            The phone of the customer

        Returns
        -------
        dict
            a dict containing success/error message
        """
        if name:
            if not self.database_dict.get(name):
                self.database_dict.update({name: {
                    'name': name,
                    'age': age,
                    'address': address,
                    'phone': phone,
                }})

                ans_dict = {'message': 'Customer has been added',
                            'success': True}
            else:
                ans_dict = {'message': 'Customer already exists'}
        else:
            ans_dict = {'message': 'Please provide Customer name'}
        return ans_dict

    def delete_customer(self, name=''):
        """It takes customer name to remove the customer data from the 
        server if name is already exists and return the success message
        Otherwise return error message

        Parameters
        ----------
        name : str
            The name of the customer

        Returns
        -------
        dict
            a dict containing success/error message
        """
        if name:
            if self.database_dict.get(name):
                del self.database_dict[name]
                ans_dict = {'message': 'Customer has been deleted',
                            'success': True}
            else:
                ans_dict = {'message': 'Customer does not exists'}
        else:
            ans_dict = {'message': 'Please provide Customer name'}
        return ans_dict

    def update_customer_age(self, name='', age=''):
        """It takes customer name and age to update the customer age if 
        customer name is already exists and return the success message
        Otherwise return error message

        Parameters
        ----------
        name : str
            The name of the customer
        age : str
            The age of the customer

        Returns
        -------
        dict
            a dict containing success/error message
        """
        if name:
            if self.database_dict.get(name):
                data_dict = self.database_dict.get(name)
                data_dict.update({'age': age})
                self.database_dict.update({name: data_dict})
                ans_dict = {'message': 'Customer age has been updated',
                            'success': True}
            else:
                ans_dict = {'message': 'Customer not found'}
        else:
            ans_dict = {'message': 'Please provide Customer name'}
        return ans_dict

    def update_customer_address(self, name='', address=''):
        """It takes customer name and address to update the customer address if 
        customer name is already exists and return the success message
        Otherwise return error message

        Parameters
        ----------
        name : str
            The name of the customer
        address : str
            The address of the customer

        Returns
        -------
        dict
            a dict containing success/error message
        """
        if name:
            if self.database_dict.get(name):
                data_dict = self.database_dict.get(name)
                data_dict.update({'address': address})
                self.database_dict.update({name: data_dict})
                ans_dict = \
                    {'message': 'Customer address has been updated',
                     'success': True}
            else:
                ans_dict = {'message': 'Customer not found'}
        else:
            ans_dict = {'message': 'Please provide Customer name'}
        return ans_dict

    def update_customer_phone(self, name='', phone=''):
        """It takes customer name and phone to update the customer phone if 
        customer name is already exists and return the success message
        Otherwise return error message

        Parameters
        ----------
        name : str
            The name of the customer
        phone : str
            The phone of the customer

        Returns
        -------
        dict
            a dict containing success/error message
        """
        if name:
            if self.database_dict.get(name):
                data_dict = self.database_dict.get(name)
                data_dict.update({'phone': phone})
                self.database_dict.update({name: data_dict})
                ans_dict = \
                    {'message': 'Customer phone has been updated',
                     'success': True}
            else:
                ans_dict = {'message': 'Customer not found'}
        else:
            ans_dict = {'message': 'Please provide Customer name'}
        return ans_dict

    def sort_database(self):
        """It sorts the customer data based on customer name

        Returns
        -------
        dict
            a dict containing customers data
        """
        keys = sorted(self.database_dict, key=str.lower)
        res_data_dict = {}
        for key in keys:
            res_data_dict.update({key: self.database_dict.get(key)})
        return res_data_dict

    def read_file(self, path_name='data.txt'):
        """It takes file path and load the customer data into the server
    
        Parameters
        ----------
        path_name : str
            The path file
        """
        with open(path_name, 'r') as data_file:
            for line in data_file:

                value_dict = {
                    'name': '',
                    'age':'',
                    'address':'',
                    'phone':''
                }

                line = line.split('|')
                try:
                    name = line[0].strip()
                except Exception:
                    name = ''
                    pass

                if not name or self.database_dict.get(name):
                    continue

                try:
                    age = int(line[1].strip())
                except Exception:
                    age = ''
                    pass

                try:
                    address = line[2].strip()
                except Exception:
                    address = ''
                    pass

                try:
                    phone = line[3].strip()
                except Exception:
                    phone = ''
                    pass

                value_dict.update({'name': name})
                value_dict.update({'age': age})
                value_dict.update({'address': address})
                value_dict.update({'phone': phone})

                self.database_dict.update({name: value_dict})


class Server(socketserver.BaseRequestHandler):
    """
    A class used to communicate with client via socket programming
    """
    def handle(self):

        server_operation_obj = self.server.server_operation_obj

        while True:
            try:
                # checking data recieved from client
                data = self.request.recv(65536)
                if not data:
                    break

                req_dict = json.loads(data.decode('utf-8'))
                choice = req_dict.get('choice', None)

                if choice == '1':
                    # To find customer data
                    res_data_dict = \
                        server_operation_obj.get_customer(req_dict.get('name'
                            , ''))
                    self.request.sendto(json.dumps(res_data_dict).encode('utf-8'
                            ), self.client_address)

                elif choice == '2':
                    # To add customer data
                    name = req_dict.get('name', '')
                    age = req_dict.get('age', '')
                    address = req_dict.get('address', '')
                    phone = req_dict.get('phone', '')
                    res_data_dict = \
                        server_operation_obj.add_customer(name, age,
                            address, phone)
                    self.request.sendto(json.dumps(res_data_dict).encode('utf-8'
                            ), self.client_address)

                elif choice == '3':
                    # To delete specific customer data
                    res_data_dict = \
                        server_operation_obj.delete_customer(req_dict.get('name'
                            , ''))
                    self.request.sendto(json.dumps(res_data_dict).encode('utf-8'
                            ), self.client_address)

                elif choice == '4':
                    # To update customer age
                    name = req_dict.get('name', '')
                    age = req_dict.get('age', '')
                    res_data_dict = \
                        server_operation_obj.update_customer_age(name,
                            age)
                    self.request.sendto(json.dumps(res_data_dict).encode('utf-8'
                            ), self.client_address)

                elif choice == '5':
                    # To update customer address
                    name = req_dict.get('name', '')
                    address = req_dict.get('address', '')
                    res_data_dict = \
                        server_operation_obj.update_customer_address(name,
                            address)
                    self.request.sendto(json.dumps(res_data_dict).encode('utf-8'
                            ), self.client_address)

                elif choice == '6':
                    # To update customer phone
                    name = req_dict.get('name', '')
                    phone = req_dict.get('phone', '')
                    res_data_dict = \
                        server_operation_obj.update_customer_phone(name,
                            phone)
                    self.request.sendto(json.dumps(res_data_dict).encode('utf-8'
                            ), self.client_address)

                elif choice == '7':
                    # To sort and return customer data
                    res_data_dict = server_operation_obj.sort_database()
                    self.request.sendto(json.dumps(res_data_dict).encode('utf-8'
                            ), self.client_address)

            except Exception as e:
                break


if __name__ == '__main__':
    
    HOST_NAME = 'localhost'
    PORT = 9999

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    with socketserver.TCPServer((HOST_NAME, PORT), Server) as server:
        try:
            server.server_operation_obj = ServerOperations()
            print("Server is running !")
            server.serve_forever()
        except Exception as e:
            print(e)