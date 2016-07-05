'''
Created on Jun 10, 2016

@author: Thomas Adriaan Hellinger
'''
import argparse
import os
import sys

from IPython import embed
from yapsy.PluginManager import PluginManager


class App(object):

    def __init__(self):
        self.plugins = {}
        # Build the manager
        self.simplePluginManager = PluginManager()
        # Tell it the default place(s) where to find plugins
        self.simplePluginManager.setPluginPlaces([
            os.path.join(os.getcwd(), "simulations", "scenario_plugins")
        ])
        # Load all plugins
        self.simplePluginManager.collectPlugins()
        
        for pluginInfo in self.simplePluginManager.getAllPlugins():
            self.simplePluginManager.activatePluginByName(pluginInfo.name)
            self.plugins[pluginInfo.name] = pluginInfo.plugin_object
            nickname = pluginInfo.details['Documentation'].get('nickname')
            if nickname:
                self.plugins[nickname] = pluginInfo.plugin_object
        
        parser = argparse.ArgumentParser(
            prog="RoodeStem",
            description='Voting system implementation and simulator',
            usage='''app <command> [<args>]

RoodeStem commands are:
   scenario    Manage scenarios
''')
        parser.add_argument('command', help='Subcommand to run')
        # parse_args defaults to [1:] for args, but you need to
        # exclude the rest of the args too, or validation will fail
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print('Unrecognized command')
            parser.print_help()
            exit(1)
        # use dispatch pattern to invoke method with same name
        getattr(self, args.command)()

    def scenario(self):
        parser = argparse.ArgumentParser(
            description='Manages or runs scenarios')
        # prefixing the argument with -- means it's optional
        parser.add_argument('--list', action='store_true')
        
        subparsers = parser.add_subparsers(dest='subparser_name')
        run_parser = subparsers.add_parser('run')
        run_parser.add_argument('scenario_name', metavar='scenario',
                                help="Scenario name or nickname")
        run_parser.add_argument('-v', '--voters', required=False, type=int,
                                help="Number of voters")
        run_parser.add_argument('-c', '--candidates', required=False, 
                                nargs='*', help='Candidate names')
        
        args = parser.parse_args(sys.argv[2:])
        if args.list:
            print()
            print("="*10 + " Available plugins " + "="*10)
            print()
            for pluginInfo in self.simplePluginManager.getAllPlugins():
                nickname = pluginInfo.details['Documentation'].get('nickname')
                if nickname:
                    nickname = " (AKA "+ nickname +")"  
                print("*    " + pluginInfo.name + nickname)
            print()
            print("="*10 + len(" Available plugins ")*'=' + "="*10)
            print()
        else:
            scplugin = self.plugins[args.scenario_name]
            if args.candidates:
                scplugin.choices = args.candidates
            if args.voters:
                scplugin.run(args.voters)
            else:
                scplugin.run()
            
if __name__ == '__main__':
    App()
    
#     embed()