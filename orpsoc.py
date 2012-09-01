#!/usr/bin/python
import argparse

from orpsoc import System
from orpsoc.Config import Config
from orpsoc.simulator import SimulatorFactory
from orpsoc.System import System
from orpsoc.Core import Core
import os

def list_cores(args):
    cores = Config().get_cores()
    print("Available cores:")
    for core in cores:
        print(core, Core(cores[core]).cache_status())

def list_systems(args):
    print("Available systems:")
    for system in Config().get_systems():
        print(system)

def sim(args):
    if not args.sim:
        args.sim=['icarus']
    
    system = System(Config().get_systems()[args.system],
                    Config().cores_root)

    sim = SimulatorFactory(args.sim[0], system)
    sim.prepare()
    if args.testcase:
        sim.run(os.path.join(os.getcwd(), args.testcase[0]))

if __name__ == "__main__":

    config = Config()
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    #General options
    parser_list_systems = subparsers.add_parser('list-systems', help='List available systems')
    parser_list_systems.set_defaults(func=list_systems)

    parser_list_cores = subparsers.add_parser('list-cores', help='List available cores')
    #parser_list_cores.
    parser_list_cores.set_defaults(func=list_cores)

    #Simulation subparser
    parser_sim = subparsers.add_parser('sim', help='Setup and run a simulation')
    parser_sim.add_argument('--sim', nargs=1)
    parser_sim.add_argument('--testcase', nargs=1)
    parser_sim.add_argument('--dry-run', action='store_true')
    parser_sim.add_argument('system')
    parser_sim.set_defaults(func=sim)

    p = parser.parse_args()
    p.func(p)