"""Appflow Automation Utility"""
import pandas as pd
from troposphere import Template, Ref, Tags
import troposphere.appflow as appflow
import yaml

def create_appflow(title, flow_name, flow_list, data_type,
                   description, trigger_type, src_connector_type,
                   connector_profile_name, obj, enable_dynamic_field_update,
                   include_deleted_records, tgt_connector_type, bucket_name,
                   bucket_prefix, file_type, aggregation_type, data_pull_mode,
                   end_time, schedule, start_time, time_zone):
    """Create Appflow"""
    prefix = 'edbccmpcp'
    app_flow = appflow.Flow('r' + prefix + title + 'appflowcft')
    # app_flow = appflow.Flow('rEdbCCMAppflow')
    app_flow.FlowName = flow_name
    app_flow.Description = description
    # app_flow.KMSArn = Ref('pKMSArn')

    # Creating the source config for Salesforce
    salesforce_conn_prop = appflow.SalesforceSourceProperties()
    salesforce_conn_prop.Object = obj
    salesforce_conn_prop.EnableDynamicFieldUpdate = enable_dynamic_field_update
    salesforce_conn_prop.IncludeDeletedRecords = include_deleted_records

    #incremental_pull_cofig.DatetimeTypeFieldName = 'LastModifiedDate'
    source_conn_prop = appflow.SourceConnectorProperties()
    source_conn_prop.Salesforce = salesforce_conn_prop
    source_flow_config = appflow.SourceFlowConfig()
    source_flow_config.ConnectorType = src_connector_type
    source_flow_config.ConnectorProfileName = Ref(connector_profile_name)
    source_flow_config.SourceConnectorProperties = source_conn_prop
    app_flow.SourceFlowConfig = source_flow_config
    # Creating the destination flow config
    s3_conn_prop = appflow.S3DestinationProperties()
    destination_connector_prop = appflow.DestinationConnectorProperties()
    destination_flow_config_list = appflow.DestinationFlowConfig()
    destination_flow_config_list.ConnectorType = tgt_connector_type
    destination_flow_config_list.DestinationConnectorProperties = destination_connector_prop
    destination_connector_prop.S3 = s3_conn_prop
    s3_conn_prop.BucketName = Ref(bucket_name)
    s3_conn_prop.BucketPrefix = Ref(bucket_prefix)
    s3_conn_prop.S3OutputFormatConfig = appflow.S3OutputFormatConfig()
    s3_conn_prop.S3OutputFormatConfig.FileType = file_type
    s3_conn_prop.S3OutputFormatConfig.AggregationConfig = appflow.AggregationConfig()
    s3_conn_prop.S3OutputFormatConfig.AggregationConfig.AggregationType = aggregation_type
    app_flow.DestinationFlowConfigList = [destination_flow_config_list]
    # Adding projection task
    task1 = appflow.Task()
    task1.SourceFields = flow_list.split('|')
    task1.TaskType = "Filter"
    task1.ConnectorOperator = appflow.ConnectorOperator()
    task1.ConnectorOperator.Salesforce = 'PROJECTION'
    app_flow.Tasks = [task1]
    #Adding Tags
    tags = Tags({"pCostCenter": Ref('pCostCenter')},
                {"pCostCenterApprover": Ref('pCostCenterApprover')},
                {"pSystemOwner": Ref('pSystemOwner')},
                {"pSystemCustodian": Ref('pSystemCustodian')},
                {"pPrimaryItContact": Ref('pPrimaryItContact')},
                {"pLevel1BusinessArea": Ref('pLevel1BusinessArea')},
                {"pDataClassification": Ref('pDataClassification')},
                {"pHipaa": Ref('pHipaa')},
                # {"pOrg": org},
                {"pApplicationCi": Ref('pApplicationCi')})
    app_flow.Tags = tags

    #Adding Map task
    for i in range(len(flow_list.split('|'))):
        task = appflow.Task()
        task.TaskType = "Map"
        lst = []
        lst.append({'Key':'SOURCE_DATA_TYPE', 'Value':data_type.split('|')[i]})
        lst.append({'Key':'DESTINATION_DATA_TYPE', 'Value':data_type.split('|')[i]})
        lst = yaml.dump(lst)
        # print(lst)
        task_prop1 = appflow.TaskPropertiesObject()
        task_prop1.Key = 'SOURCE_DATA_TYPE'
        task_prop1.Value = data_type.split('|')[i]
        task_prop2 = appflow.TaskPropertiesObject()
        task_prop2.Key = 'DESTINATION_DATA_TYPE'
        task_prop2.Value = data_type.split('|')[i]
        task.TaskProperties = [task_prop1, task_prop2]
        task.SourceFields = [flow_list.split('|')[i]]
        task.DestinationField = flow_list.split('|')[i]
        task.ConnectorOperator = appflow.ConnectorOperator()
        task.ConnectorOperator.Salesforce = 'NO_OP'
        app_flow.Tasks.append(task)

    #Adding trigger
    if trigger_type == 'Event' or trigger_type == 'onDemand':
        trigger = appflow.TriggerConfig()
        trigger.TriggerType = trigger_type
        app_flow.TriggerConfig = trigger
        # print(app_flow.TriggerConfig)
    elif trigger_type == 'Scheduled':
        trigger = appflow.TriggerConfig()
        trigger.TriggerType = trigger_type
        schedule_trigger_prop = appflow.ScheduledTriggerProperties()
        schedule_trigger_prop.DataPullMode = data_pull_mode
        schedule_trigger_prop.ScheduleEndTime = end_time
        schedule_trigger_prop.ScheduleExpression = schedule
        schedule_trigger_prop.ScheduleStartTime = start_time
        schedule_trigger_prop.TimeZone = time_zone
        trigger.TriggerProperties = schedule_trigger_prop
        app_flow.TriggerConfig = trigger

    return app_flow

def main():
    """ Reading Config """
    config = pd.read_csv("one.csv", encoding='utf-8')
    template = Template()
    for index, row in config.iterrows(): # pylint:disable=unused-variable
        flow = create_appflow(row["Title"], row["Flow Name"], row["Field_List"],
                              row["Data_Type"], row["Description"], row["TriggerType"],
                              row["SrcConnectorType"], row["ConnectorProfileName"],
                              row["Object"], row["EnableDynamicFieldUpdate"],
                              row["IncludeDeletedRecords"], row["TgtConnectorType"],
                              row["BucketName"], row["BucketPrefix"], row["FileType"],
                              row["AggregationType"], row["Pull_Mode"], row["End_Time"],
                              row["Schedule"], row["Start_Time"], row["Time_Zone"])
        template.add_resource(flow)
    # print(template.to_dict())
    dict_data = template.to_dict()
    
    with open('appflow_resources.yaml', 'w') as file:
        yaml.dump(dict_data, file, sort_keys=False, default_flow_style=False, encoding='utf-8')

if __name__ == "__main__":
    main()
