import sys, math


state_p = {}

state_action_state_p = {}

state_observation_p = {}

sequence = []

state_dict, action_dict, observation_dict = {}, {}, {}



def read_state_weights(filename):
    global state_p
    with open(filename, "r") as file:
        line = file.readline()
        line = file.readline().split()
        number = int(line[0])
        #number, weight = int(line[0]), int(line[1])
        
        total_weight = 0
        for i in range(number):
            line = file.readline().split()
            state, weight = line[0], int(line[1])
            state_p[state] = weight
            
            total_weight += weight
        
        # calculate the probability
        for state in state_p:
            state_p[state] /= 1.0*total_weight
    
    print("state_p")
    print(state_p)
    print("\n")
            

def read_state_action_state_weights(filename):
    global state_action_state_p, state_dict, action_dict
    with open(filename, "r") as file:
        line = file.readline()
        line = file.readline().split()
        number, number_states = int(line[0]), int(line[1])
        number_actions, default_weight = int(line[2]), int(line[3])
        
        for i in range(number):
            line = file.readline().split()
            #print( line )
            state, action, next_state, weight = line[0], line[1], line[2], int(line[3])
            state_action_state_p[(state,action,next_state)] = weight
            
            state_dict[state] = True
            state_dict[next_state] = True
            action_dict[action] = True
    
        # calculate the probability
        for state1 in state_dict:
            for action in action_dict:
                total_weight = 0.0
                for state2 in state_dict:
                    key = (state1, action, state2)
                    if key not in state_action_state_p:
                        state_action_state_p[key] = default_weight

                    total_weight += state_action_state_p[key]
                
                for state2 in state_dict:
                    key = (state1, action, state2)
                    state_action_state_p[key] /= total_weight
    print("state_action_state_p")
    print( state_action_state_p )
    print("\n")


def read_state_observation_weights(filename):
    global state_observation_p, state_dict, observation_dict
    with open(filename, "r") as file:
        line = file.readline()
        line = file.readline().split()
        number, number_states = int(line[0]), int(line[1])
        number_observations, default_weight = int(line[2]), int(line[3])
        
        for i in range(number):
            line = file.readline().split()
            #print( line )
            state, observation, weight = line[0], line[1], int(line[2])
            state_observation_p[(state,observation)] = weight
            
            state_dict[state] = True
            observation_dict[observation] = True
        
        # calculate the probability
        for state in state_dict:
            total_weight = 0.0
            for observation in observation_dict:
                key = (state, observation)
                if key not in state_observation_p:
                    state_observation_p[key] = default_weight
                
                total_weight += state_observation_p[key]
            
            for observation in observation_dict:
                key = (state, observation)
                state_observation_p[key] /= total_weight
    
    print("state_observation_p")
    print( state_observation_p )
    print("\n")


def read_observation_actions(filename):
    global sequence
    with open(filename, "r") as file:
        line = file.readline()
        line = file.readline().split()
        number = int(line[0])
        for i in range(number):
            line = file.readline().split()
            #print( line )
            sequence.append( line[0] )
            if len(line)==2:
                sequence.append( line[1] )
    print("sequence")
    print( sequence )
    print("\n")


def viterbi( filename ):
    n = len(sequence)
    P = []
    for i in range(0,n,2):
        Pi = {state: [0.0, []] for state in state_dict}
        if i==0:
            observation = sequence[i]
            for state in state_dict:
                Pi[state][0] = state_p[state] * state_observation_p[(state,observation)]
                Pi[state][1] = [state]
        else:
            action, observation = sequence[i-1], sequence[i]
            for state in state_dict:
                max_p, max_path = 0.0, []
                for last_state in state_dict:
                    # last_state -> action -> state (observation)
                    p, path = P[-1][last_state][0], [ s for s in P[-1][last_state][1] ]
                    p *= state_action_state_p[(last_state,action,state)]
                    p *= state_observation_p[(state,observation)]
                    path.append( state )
                    
                    if max_p < p:
                        max_p, max_path = p, path
                Pi[state] = [max_p, max_path]
        
        P.append( Pi )
    
    
    max_p, target_path = 0.0, []
    for state in P[-1]:
        if max_p < P[-1][state][0]:
            max_p, target_path = P[-1][state][0], P[-1][state][1]
    
    print("target_path")
    print( target_path )
    print("\n")
    
    
    with open(filename, "w") as file:
        file.write("states\n")
        file.write(str(len(target_path))+"\n")
        #print("states")
        #print(len(target_path))
        for state in target_path:
            file.write(state+"\n")
            #print( state )
    #print( P[-1] )





# python work.py state_weights.txt state_action_state_weights.txt state_observation_weights.txt observation_actions.txt

# python work.py little_prince/test_case_1/state_weights.txt little_prince/test_case_1/state_action_state_weights.txt little_prince/test_case_1/state_observation_weights.txt little_prince/test_case_1/observation_actions.txt

# python work.py little_prince/test_case_2/state_weights.txt little_prince/test_case_2/state_action_state_weights.txt little_prince/test_case_2/state_observation_weights.txt little_prince/test_case_2/observation_actions.txt

# python work.py speech_recognition/test_case_1/state_weights.txt speech_recognition/test_case_1/state_action_state_weights.txt speech_recognition/test_case_1/state_observation_weights.txt speech_recognition/test_case_1/observation_actions.txt



if __name__ == "__main__":
    state_weights_file = "state_weights.txt"
    state_action_state_weights_file = "state_action_state_weights.txt"
    state_observation_weights_file = "state_observation_weights.txt"
    observation_actions_file = "observation_actions.txt"
    output_file = "states.txt"
    
    read_state_weights(state_weights_file)
    
    read_state_action_state_weights(state_action_state_weights_file)
    
    read_state_observation_weights(state_observation_weights_file)
    
    read_observation_actions( observation_actions_file )

    viterbi( output_file )
    
