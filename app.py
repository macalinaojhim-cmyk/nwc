
import streamlit as st 
import pandas as pd
    

st.title("🚚Delivery cost Minimization")

st.subheader("Supply")

supplier_data = {
  "Supplier" : ["Warehouse A", "Warehouse B", "Warehouse C"],
  "Supply" : [
      st.number_input("Supply to Warehouse A",value = 60, min_value = 10, step = 1),
      st.number_input("Supply to Warehouse B",value = 40, min_value = 10, step = 1), 
      st.number_input("Supply to Warehouse C",value = 50, min_value = 10, step = 1)
      ],
}

st.table(supplier_data)

st.write("")
st.subheader("Demand")

demand_data = {
    "Demands" : ["Demand A", "Demand B", "Demand C"],
    "Demand" : [
        st.number_input("Demand A", value = 70, min_value = 10, step = 1),
        st.number_input("Demand B", value = 45, min_value = 10, step = 1),
        st.number_input("Demand C", value = 35, min_value = 10, step = 1)
        ]
}

st.table(demand_data)

delivery_cost = {
    "Warehouse A" : {
        "Demand A" : 100,
        "Demand B" : 130,
        "Demand C" : 180
    },
    "Warehouse B" : {
        "Demand A" : 120,
        "Demand B" : 90,
        "Demand C" : 190
    },
    "Warehouse C" : {
        "Demand A" : 100,
        "Demand B" : 170,
        "Demand C" : 85
    }
}


st.table(delivery_cost)


total_supply = sum(supplier_data["Supply"])
total_demand = sum(demand_data["Demand"])

st.caption("In transportation problem, total supply must equal to toal demand")

st.write("Total Supply = ", total_supply)
st.write("Total Demand = ", total_demand)

if total_supply == total_demand:
    st.success("Problem is Balanced")

    sA, sB, sC = supplier_data["Supply"]
    dA, dB, dC = demand_data["Demand"]

    sA, sB, sC = supplier_data["Supply"]
    dA, dB, dC = demand_data["Demand"]


    x_AA = min(sA, dA)
    sA -= x_AA
    dA -= x_AA

    x_BA = min(sB, dA)
    sB -= x_BA
    dA -= x_BA

    x_BB = min(sB, dB)
    sB -= x_BB
    dB -= x_BB

    x_CB = min(sC, dB)
    sC -= x_CB
    dB -= x_CB

    x_CC = min(sC, dC)
    sC -= x_CC
    dC -= x_CC

    st.subheader("North West Corner Table (NWC)")
    nwc_table = {
        "Warehouse" : [
            "Warehouse A", "Warehouse B", "Warehouse C"
        ],
        "Demand A" : [x_AA, x_BA, 0],
        "Demand b" : [0, x_BB, x_CB],
        "Demand C" : [0, 0, x_CC]
    }

    nwc_cost_table = {
        "Warehouses" : ["Warehouse A", "Warehouse B", "Warehouse C", "Demand"],

        "Demand A" : [
            delivery_cost["Warehouse A"]["Demand A"],
            delivery_cost["Warehouse B"]["Demand A"],
            delivery_cost["Warehouse C"]["Demand A"],

            demand_data["Demand"][0],
            ],

        "Demand B" : [
            delivery_cost["Warehouse A"]["Demand B"],
            delivery_cost["Warehouse B"]["Demand B"],
            delivery_cost["Warehouse C"]["Demand B"],
            
            demand_data["Demand"][1],
            ],
        "Demand C" : [
            delivery_cost["Warehouse A"]["Demand C"],
            delivery_cost["Warehouse B"]["Demand C"],
            delivery_cost["Warehouse C"]["Demand C"],
            
            demand_data["Demand"][2]
            ],

        "Supply" : [
            supplier_data["Supply"][0],
            supplier_data["Supply"][1],
            supplier_data["Supply"][2],
            ""
        ]
    }

    st.table(nwc_table)
    df = pd.DataFrame(nwc_cost_table).set_index("Warehouses")
    st.dataframe(df)
    
    st.subheader("Total Cost (Northwest Corner)")

    nwc_total_cost = (
    x_AA * delivery_cost["Warehouse A"]["Demand A"] +
    x_BA * delivery_cost["Warehouse B"]["Demand A"] +
    x_BB * delivery_cost["Warehouse B"]["Demand B"] +
    x_CB * delivery_cost["Warehouse C"]["Demand B"] +
    x_CC * delivery_cost["Warehouse C"]["Demand C"]
)

    st.success(f"Total Transportation Cost = ₱ {nwc_total_cost}")

else: 
    st.error("Problem is not balanced")


