-- DELETE 语句基于查询条件: select * from t_tool_index where index_id ='716aa4d7e7bd45a284c9dfcdb20d0eda';
DELETE FROM t_tool_index WHERE where index_id ='716aa4d7e7bd45a284c9dfcdb20d0eda';;

-- 原始查询: select * from t_tool_index where index_id ='716aa4d7e7bd45a284c9dfcdb20d0eda';
INSERT INTO t_tool_index (index_id, index_code, index_name, index_type, rule_meta_id, index_code_alias, index_name_alias, category_id, category_code, report_id, report_code, tpl_id, index_range, is_mapping, is_float, is_float_header, float_index_code, is_professional, float_match_type, float_match_relation, float_match_content, format_rule_id, format_rule_name, result_type, cumulative_type, sum_type, master_table_id, master_table_name, master_table_name_label, value_column_id, value_column_name, value_column_name_label, join_column_id, join_column_name, join_column_name_label, operation_type, slave_table_id, slave_table_name, slave_table_name_label, slave_column_id, slave_column_name, join_type, condition_json, condition_sql, full_sql, expression, md5, is_tag, tag_id, tag, tag_name, solution, memo, enable_status, is_valid, tenant_code, create_time, create_user_id, create_user_name, update_time, update_user_id, update_user_name, reserved1, reserved2, reserved3, reserved4, reserved5, reserved6, reserved7, reserved8, reserved9, reserved10, pre_handler_rule, after_handler_rule, index_version) VALUES
('516aa4d7e7bd45a284c9dfcdb20d0eda', 'EIT_FORM_ATT38_A02', '税款所属期间', '2', NULL, NULL, NULL, 'a9639c714d75489bb23284eb73594913', '10104', '7701ecc49b9c4a4fb4e0670235a148aa', '10104202', 'dafc73471ee046918c107c79de2fd7fa', NULL, NULL, 0, 0, NULL, 0, NULL, NULL, NULL, '0bbd0bea71f94ef9b8a1f524f0c11162', '原值输出', 'string', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '{"categoryCode":"10104","categoryId":"a9639c714d75489bb23284eb73594913","expression":"if(@申报周期()  ==  ''period_season'')\r\n{\r\nstart=@所属季度起始日期();\r\nend=@所属季度终止日期();\r\nreturn \\"税款所属期间：\\"+ @日期(start,''yyyy年MM月dd日'') + \\" 至 \\" + @日期(end,''yyyy年MM月dd日'');\r\n}else  if(@申报周期()  ==  ''period_half_year''){\r\nstart  =  @所属期半年起始日期();\r\nend  =  @所属期半年终止日期();\r\nreturn  \\"税款所属期间：\\"+ @日期(start,''yyyy年MM月dd日'')  +  \\"至  \\"+  @日期(end,''yyyy年MM月dd日'');\r\n}else  if(@申报周期()  ==  ''period_year''){\r\nreturn  \\"税款所属期间：\\"+ @所属期间年份()+\\"年01月01日  至  \\"+  @所属期间年份()+\\"年12月31日\\";\r\n}else{\r\nstart  =  @指定月份起始日期(@所属期间());\r\nend  =  @指定月份终止日期(@所属期间());\r\nreturn  \\"税款所属期间：\\"+ @日期(start,''yyyy年MM月dd日'')  +  \\"至  \\"+  @日期(end,''yyyy年MM月dd日'');\r\n}","formatRuleId":"0bbd0bea71f94ef9b8a1f524f0c11162","formatRuleName":"原值输出","indexCode":"EIT_FORM_ATT38_A02","indexId":"716aa4d7e7bd45a284c9dfcdb20d0eda","indexName":"税款所属期间","indexType":"2","isFloatHead":"0","isFloatLine":"0","mappingIndex":"0","mappingIndexCode":false,"reportCode":"10104202","reportId":"7701ecc49b9c4a4fb4e0670235a148aa","reportName":"企业所得税汇算清缴申报表（分行）","resultType":"string","tplId":"dafc73471ee046918c107c79de2fd7fa","tplName":"A109010 企业所得税汇总纳税分支机构所得税分配表"}', NULL, NULL, 'if(@申报周期()  ==  ''period_season'')
{
start=@所属季度起始日期();
end=@所属季度终止日期();
return "税款所属期间："+ @日期(start,''yyyy年MM月dd日'') + " 至 " + @日期(end,''yyyy年MM月dd日'');
}else  if(@申报周期()  ==  ''period_half_year''){
start  =  @所属期半年起始日期();
end  =  @所属期半年终止日期();
return  "税款所属期间："+ @日期(start,''yyyy年MM月dd日'')  +  "至  "+  @日期(end,''yyyy年MM月dd日'');
}else  if(@申报周期()  ==  ''period_year''){
return  "税款所属期间："+ @所属期间年份()+"年01月01日  至  "+  @所属期间年份()+"年12月31日";
}else{
start  =  @指定月份起始日期(@所属期间());
end  =  @指定月份终止日期(@所属期间());
return  "税款所属期间："+ @日期(start,''yyyy年MM月dd日'')  +  "至  "+  @日期(end,''yyyy年MM月dd日'');
}', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, '100', '2022-12-23 02:40:18', 'fa0895bb68754ac4b238e692ceb5e77f', '管理员', '2023-01-16 15:40:23', 'PAUTAX', '沐趁堰', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 2);