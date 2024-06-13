# bes_data_dashborad

## concept

```mermaid
%%{ init: { 'flowchart': { 'curve': 'basis' } } }%%
flowchart LR;
    subgraph gov_dbaas
        subgraph mariadb
            sql_procedure
            mertic_data_table
        end
    end
    subgraph trust_k8s_cluster
        mariadb-data-collector
    end
    subgraph elasticsearch
        elastic_index[index: data-metrics-*]
    end

sql_procedure --> mertic_data_table
mariadb-data-collector --> sql_procedure
mertic_data_table --> mariadb-data-collector

mariadb-data-collector --> elastic_index
elastic_index --> grafana
```

1. `mariadb-data-collector` will execute sql_procedure, this sql_procedure should generate mertic data to a table.
2. than `mariadb-data-collector` send mertic data to elasticsearch. index name should start with `data-metrics-`
3. setup grafana dashboard for it

## mariadb-data-collector config

![](gitlab_mariadb_data_collector.png)
