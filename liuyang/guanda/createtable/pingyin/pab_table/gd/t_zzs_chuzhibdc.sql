CREATE TABLE t_zzs_chuzhibdc (
`chuzhibdc_id` BIGINT UNSIGNED AUTO_INCREMENT COMMENT '主键',
`ssqj` varchar(12) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '所属期间',
`zcbm` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '资产编码',
`zcms` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '资产描述',
`sfydfc` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '是否异地房产',
`czrq` varchar(12) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '处置日期',
`sfzjfc` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '是否自建房产',
`zbhrq` varchar(12) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '资本化日期',
`gzjghpgjg` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '购置价格或评估价格',
`cshsjghcsssddxj` decimal(20, 2) COMMENT '出售含税价格或出售时收到的现金',
`sfxyzfcszdyj` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '是否需要在房产所在地预缴',
`sfkyjcgzjhdrzj` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '是否可以减除购置价或抵入作价',
`jsff` varchar(12) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '计税方法',
`yjsj` varchar(12) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '预缴时间',
`yjwspzbh` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '预缴完税凭证编号',
`yzl` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '预征率',
`yjskjsjc` varchar(12) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '预缴税款计税基础',
`yjsk` decimal(20, 2) COMMENT '预缴税款',
`syslhzzsl` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '适用税率或者征收率',
`kcxqcye` decimal(20, 2) COMMENT '扣除项期初余额',
`bqsjkcje` decimal(20, 2) COMMENT '本期实际扣除金额',
`kcxqmye` decimal(20, 2) COMMENT '扣除项期末余额',
`xse` decimal(20, 2) COMMENT '销售额',
`xxynse` decimal(20, 2) COMMENT '销项应纳税额',
`kchhsxse` decimal(20, 2) COMMENT '扣除后含税销售额',
`kchxxynse` decimal(20, 2) COMMENT '扣除后销项(应纳)税额',
`bqdjse` decimal(20, 2) COMMENT '本期抵减税额',
`bqyjse` decimal(20, 2) COMMENT '本期应交税额',
`bhsxse` decimal(20, 2) COMMENT '不含税销售额',
`bdclx` varchar(12) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '不动产类型',
`ssqj` varchar(20)  CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '所属期间',
`group_no` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '机构代码',
`group_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '机构名称',
`taxpayer_no` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '纳税人识别号',
`taxpayer` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '纳税人名称',
`is_valid` tinyint NULL DEFAULT NULL COMMENT '是否有效 0:无效,1:有效[dict:is_valid]',
`enable_status` tinyint NULL DEFAULT NULL COMMENT '启用状态 0:未启用1:已启用[dict:enable_status]',
`create_user_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '创建人ID',
`create_user_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '创建人名称',
`create_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
`update_user_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '更新人ID',
`update_user_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '更新人名称',
`update_time` datetime NULL DEFAULT NULL COMMENT '更新时间',
`tenant_code` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '租户编码',
`reserved1` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '预留字段1',
`reserved2` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '预留字段2',
`reserved3` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '预留字段3',
`reserved4` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '预留字段4',
`reserved5` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '预留字段5',
`reserved6` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '预留字段6',
`reserved7` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '预留字段7',
`reserved8` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '预留字段8',
`reserved9` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '预留字段9',
`reserved10` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '预留字段10'
, PRIMARY KEY (`chuzhibdc_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT 'chuzhi不动产';
