/*
 Source Server Type    : MySQL
 Source Server Version : 50723
 Source Host           : localhost:3306
 Source Schema         : spiderdb

 Target Server Type    : MySQL
 Target Server Version : 50723
 File Encoding         : 65001

 Date: 07/04/2019 00:08:37
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;


-- ----------------------------
-- Table structure for spider_crawl_monitor
-- ----------------------------
DROP TABLE IF EXISTS `spider_crawl_monitor`;
CREATE TABLE `spider_crawl_monitor`  (
  `stat_time` datetime(0) NULL DEFAULT NULL,
  `spider_name` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `job_instance_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `task_instance_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `create_time` datetime(0) NULL DEFAULT NULL,
  `request` int(8) NULL DEFAULT NULL,
  `response` int(8) NULL DEFAULT NULL,
  `filtered_request` int(8) NULL DEFAULT NULL,
  `crawled_pages` int(8) NULL DEFAULT NULL,
  `scraped_items` int(8) NULL DEFAULT NULL,
  `status_200` int(8) NULL DEFAULT NULL,
  `status_other` int(8) NULL DEFAULT NULL,
  `critical` int(8) NULL DEFAULT NULL,
  `error` int(8) NULL DEFAULT NULL,
  `warning` int(8) NULL DEFAULT NULL,
  `redirect` int(8) NULL DEFAULT NULL,
  `retry` int(8) NULL DEFAULT NULL,
  `ignored` int(8) NULL DEFAULT NULL,
  `remark` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for spider_task_monitor
-- ----------------------------
DROP TABLE IF EXISTS `spider_task_monitor`;
CREATE TABLE `spider_task_monitor`  (
  `project_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '项目id',
  `project_name` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `version` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `job_instance_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '周期调度作业id',
  `spider_name` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `task_instance_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '爬虫任务实例id',
  `execute_ip` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `priority` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `args` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `create_time` datetime(0) NULL DEFAULT NULL,
  `status` tinyint(1) NULL DEFAULT NULL,
  `error_flag` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `remark` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
