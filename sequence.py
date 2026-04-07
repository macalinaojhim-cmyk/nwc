import pandas as pd
import numpy as np
import streamlit as st

def main():

    st.markdown("<h1 style='text-align: center;'>Sequencing Problem Calculator</h1>", unsafe_allow_html=True)
    st.subheader("-Objectives")
    st.write("-Minimize Makespan")
    st.write("-Minimize Completion Time")
    st.write("-Minimize Lateness")
    st.write("-Minimize Idle Time")
    st.subheader("Johnson's Method")
    st.subheader("Case 1:\n   --Processing n jobs thru 2 Machines")
        
    chars = "abcdefghijklmnopqrstuvwxyz"
    machines_number = st.number_input("Number of Machines: ", value=2, min_value=2, step=1)
    jobs_number = st.number_input("Number of Jobs: ", value=3, min_value=1, step=1)
    machine_worktime = []
        
    if machines_number <= 1:

        st.error("Number of Machines must be greater to 1")
        
    elif jobs_number <= 0:

        st.error("At least 1 job")

    else:
            
        for i in range(machines_number):
            
            try:

                worktime = list(map(int, st.text_input(f"Enter worktime of machine {i+1} to {jobs_number} jobs (Separated by space):(e.g. 1 2 3 4)",placeholder="e.g. 1 2 3 4 5").split()))
                machine_worktime.append(worktime)
            
            except ValueError:
            
                st.error("Invalid Input.")

        job_name = list(chars[:jobs_number])
        machine_name = ["Machine " + letter.upper() for letter in chars[:machines_number]]

    if machines_number == 2:
    
        if st.button("Calculate"):
        
            try:
                case1(machines_number, jobs_number, machine_worktime, machine_name, job_name)
        
            except ValueError:
                st.error("Invalid input. Enter Integer separated by space")
    else:
        st.warning("not supported yet")

def case1(machines_number, jobs_number, machine_worktime, machine_name, job_name):

    table = pd.DataFrame(machine_worktime, index=machine_name, columns=job_name, dtype=int)
    st.table(table) 
    st.subheader("Optimal Sequence:")

    optimal_sequence = schedule(machine_worktime, job_name)[0]
    optimal_schedule = schedule(machine_worktime, job_name)[1]

    optimal_sequence_table = pd.DataFrame({'Jobs': optimal_sequence}, index=optimal_schedule)

    st.table(optimal_sequence_table)

    st.subheader("Makespan:")

    st.table(makespan(optimal_sequence,machine_worktime,machine_name)[0])
  
    st.write(f"Total Makespan Time:  {makespan(optimal_sequence,machine_worktime, machine_name)[1]}hrs")

    st.subheader("Idle Time: ")

    st.write(f"{machine_name[0]}:   {makespan(optimal_sequence,machine_worktime, machine_name)[2]}hrs")
    
    st.write(f"{machine_name[1]}:   {makespan(optimal_sequence,machine_worktime, machine_name)[3]}hrs")

def schedule(machine_worktime, job_name):
    
    machine_worktime = np.array(machine_worktime)
    jobs = list(job_name)
    front = []
    back = []

    while machine_worktime.shape[1] > 0:

        min_index = np.unravel_index(np.argmin(machine_worktime), machine_worktime.shape)
        row, col = min_index

        job = jobs[col]

        if row == 0:

            front.append(job)

        else:

            back.insert(0, job)
            
        machine_worktime = np.delete(machine_worktime, col, axis=1)
        jobs.pop(col)

    num_seq=[]

    for i in range(len(front+back)):
        num_seq.append(i+1)
        
    seq=[]

    for j in num_seq:
        if j==1:
            seq.append("1st")
        elif j==2: 
            seq.append("2nd")
        elif j==3:
            seq.append("3rd")
        else:
            seq.append(f"{j}th")

    sched = pd.DataFrame({"Jobs":front+back},index=seq)

    return (front+ back, seq)

def makespan(sequence, machine_worktime, machine_name):

    time_p = machine_worktime[0]
    time_q = machine_worktime[1]
    jobs = sequence

    p_in = []
    p_out = []

    q_in = []
    q_out = []
            
    #sequence to number indexing
    index = [ord(letter) - ord('a') for letter in sequence]

    for i in range(len(sequence)):
        
        if i == 0:
            p_in.append(0)
            p_out.append(p_in[0]+ time_p[index[i]])

        else:
            p_in.append(p_out[i-1])
            p_out.append(p_in[i] + time_p[index[i]])

    for i in range(len(sequence)):
        
        if i == 0:
            q_in.append(p_out[i])
            q_out.append(q_in[0] + time_q[index[i]])
        else:

            if p_out[i] > q_out[i-1]:
                q_in.append(p_out[i])
                q_out.append(q_in[i] + time_q[index[i]])
            else:
                q_in.append(q_out[i-1])
                q_out.append(q_in[i] + time_q[index[i]])
            
    total_makespan=q_out[-1]

    idle_p = q_out[-1] - p_out[-1]

    idle_q = 0

    for q in range(len(q_out)):

        if q == 0:
            idle_q += q_in[0]
        else:
            if q_in[q] != q_out[q-1]:
                idle_q += q_in[q] - q_out[q-1]
            else:
                pass

    
    idle_time = {
        f"{machine_name[0]} " : idle_p,
        f"{machine_name[1]} " : idle_q
    }

    columns = pd.MultiIndex.from_tuples([
        ('','Optimal sequence'),
        (machine_name[0], 'in'),
        (machine_name[0], 'out'),
        (machine_name[1 ], 'in'),
        (machine_name[1], 'out'),
    ])

    data = []

    for items in range(len(sequence)):
        data.append([sequence[items], p_in[items], p_out[items], q_in[items], q_out[items]])
    
    new_table = pd.DataFrame(data, columns=columns)

    return (new_table,total_makespan, idle_p, idle_q)
  

if __name__ == "__main__":
    main()
